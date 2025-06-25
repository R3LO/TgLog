# -*- coding: UTF-8 -*-
from aiogram import Bot, types
from aiogram.types import Message
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, StateFilter
from state.register import RegisterState
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from aiogram.utils.keyboard import InlineKeyboardBuilder
from state.uload_log import Upload_logState
from state.upload_lotw import Upload_lotwState
from aiogram.types import FSInputFile
from state.register import PaperQSLState
from aiogram.fsm.state import default_state
from handlers.create_pdf import create_w100c_pdf, create_w100l_pdf, create_w1000b_pdf, create_w1000u_pdf, create_w25r_pdf
import sqlite3
import os
import re

# Инициализируем роутер уровня модуля
router = Router()

@router.callback_query(F.data == 'upload')
async def main_menu_upload(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.upload.main.log(), callback_data='main_log'),
    kb.button(text=i18n.upload.lotw.sync(), callback_data='lotw_log')
    kb.button(text=i18n.upload.paper.qsl(), callback_data='paper_qsl')
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(2, 1)
    await bot.send_message(callback.from_user.id, i18n.upload.title(), reply_markup=kb.as_markup())

@router.callback_query(F.data == 'main_log')
async def main_log_upload(callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await callback.message.answer(i18n.upload.file())
    await state.clear()
    await state.set_state(Upload_logState.upload_adif)

@router.message(StateFilter(Upload_logState.upload_adif))
async def upload_adif(message: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    if message.document:
        file = 'logs/' + user + '_' + str(message.from_user.id) +'.txt'
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        await message.bot.download(message.document, destination=file_path)
        file_size = os.path.getsize(file_path)
        if (file_size > 12 * 1024 * 1024):
            await bot.send_message(message.from_user.id, i18n.upload.bigfile())
            await state.clear()
            return
        # обраюботка ADIF
        await adif(file_path, message, i18n, bot)
        await state.clear()
        await bot.send_message(message.from_user.id, i18n.upload.ok())
        await bot.send_message(message.from_user.id, i18n.main.menu(), reply_markup=interlinemenu(i18n))
    else:
        await state.clear()
        kb = InlineKeyboardBuilder()
        kb.button(text=i18n.back(), callback_data='back_main_menu')
        kb.adjust(1)
        await message.reply(i18n.upload.cancel(), reply_markup=kb.as_markup())

async def adif(file_log: str, message: Message, i18n: TranslatorRunner, bot: Bot):
    '''
    Обработка ADIF основного лога
    '''
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    error = False
    file = 'logs/' + user + '_bad_log.txt'
    bad_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(bad_file_path, 'w'):   pass
    logbook = []
    try:
        raw = re.split('<EOR>|<EOH>', open(file_log, encoding="utf8", errors='ignore').read().upper(), flags=re.IGNORECASE)
    except:
        await bot.send_message(message.from_user.id, i18n.upload.wrong())
        return
    try:
        for record in raw[1:-1]:
            if (':0><' in record): record = record.replace(':0><', ':1> <')
            qso = {}
            ADIF_REC_RE = re.compile(r'<(.*?):(\d+).*?>([^<\t\f\v]+)')
            tags = ADIF_REC_RE.findall(record)
            for tag in tags:
                qso[tag[0].lower()] = tag[2][:int(tag[1])]
                if (qso[tag[0].lower()] == 'MFSK'):
                    qso[tag[0].lower()] = 'FT4'
            if ('gridsquare' not in qso): qso['gridsquare'] = None
            if ('rst_rcvd' not in qso): qso['rst_rcvd'] = None
            if ('rst_sent' not in qso): qso['rst_sent'] = None
            logbook.append(qso)
    except:
        await bot.send_message(message.from_user.id, i18n.upload.wrong())

    if len(logbook) > 0:
        sum_qso = len(logbook)
        await bot.send_message(message.from_user.id, i18n.upload.found.qso(sum_qso=sum_qso))
        data = []
        n = 0
        for i in range(len(logbook)):
            if (logbook[i].get('call') is not None) and (logbook[i].get('qso_date') is not None) and (logbook[i].get('time_on') is not None) and (logbook[i].get('band') is not None) and (logbook[i].get('mode') is not None):
                qso_date = logbook[i].get('qso_date')[:4] + '-' + logbook[i].get('qso_date')[4:6] + '-' + logbook[i].get('qso_date')[6:]
                time_on = logbook[i].get('time_on')[:2] + ':' + logbook[i].get('time_on')[2:4]
                logbook[i]['operator'] = user
                if (logbook[i].get('band') == '13CM'):
                    data.append([logbook[i].get('call'), qso_date, time_on, logbook[i].get('band'), logbook[i].get('mode'), logbook[i].get('gridsquare'), logbook[i].get('operator'), logbook[i].get('rst_rcvd'), logbook[i].get('rst_sent')])
                    n += 1
            else:
                error = True
                txt = '---=== Wrong QSO ===---\n' + '; '.join([f'{key.capitalize()}: {value}' for key, value in logbook[i].items()]) + '\n\n'
                with open(bad_file_path, 'a', encoding='utf-8') as f:
                    f.write(txt)
        db.add_table_user(user)
        db.add_user_qso_data(user, data)
        await bot.send_message(message.from_user.id, i18n.upload.db(n=n))
        if error:
            await bot.send_message(message.from_user.id, i18n.upload.errors())
            document = FSInputFile(bad_file_path)
            await bot.send_document(message.from_user.id, document)
    else:
        await bot.send_message(message.from_user.id, i18n.upload.wrong())
        return

# ------------------------------------------------------------------------------
@router.callback_query(F.data == 'lotw_log')
async def lotw_log_upload(callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    '''
    Кнопка Синхронизация с LoTW
    '''
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, i18n.upload.lotw())
    await state.clear()
    await state.set_state(Upload_lotwState.upload_adif_lotw)

@router.message(StateFilter(Upload_lotwState.upload_adif_lotw))
async def upload_adif_lotw(message: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    '''
    Обработка загруженого ADIF LoTW

    '''
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    if message.document:
        file = 'logs/' + user + '_' + str(message.from_user.id) +'_lotw.txt'
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        await message.bot.download(message.document, destination=file_path)
        file_size = os.path.getsize(file_path)
        if (file_size > 12 * 1024 * 1024):
            await bot.send_message(message.from_user.id, i18n.upload.bigfile())
            await state.clear()
            return
        await lotw(file_path, message, i18n, bot)
        await state.clear()
        await bot.send_message(message.from_user.id, i18n.upload.ok())
        await bot.send_message(message.from_user.id, i18n.main.menu(), reply_markup=interlinemenu(i18n))
    else:
        await state.clear()
        kb = InlineKeyboardBuilder()
        kb.button(text=i18n.back(), callback_data='back_main_menu')
        kb.adjust(1)
        await message.reply(i18n.upload.cancel(), reply_markup=kb.as_markup())


async def lotw(file_path: str, message: Message, i18n: TranslatorRunner, bot: Bot):
    '''
    Обработка LoTW ADIF файла
    '''
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    logbook = []
    raw = re.split('<EOR>|<EOH>', open(file_path, encoding="utf8", errors='ignore').read().upper(), flags=re.IGNORECASE)
    if (raw[0].split('\n')[0] == 'ARRL LOGBOOK OF THE WORLD STATUS REPORT'):
        try:
            for record in raw[1:-1]:
                if (':0><' in record): record = record.replace(':0><', ':1> <')
                qso = {}
                ADIF_REC_RE = re.compile(r'<(.*?):(\d+).*?>([^<\t\f\v]+)')
                tags = ADIF_REC_RE.findall(record)
                for tag in tags:
                    qso[tag[0].lower()] = tag[2][:int(tag[1])]
                    if (qso[tag[0].lower()] == 'MFSK'):
                        qso[tag[0].lower()] = 'FT4'
                if ('gridsquare' not in qso): qso['gridsquare'] = None
                if ('state' not in qso): qso['state'] = None
                if ('operator' not in qso): qso['operator'] = user
                logbook.append(qso)
        except:
            await bot.send_message(message.from_user.id, i18n.upload.wrong())
    else:
        await bot.send_message(message.from_user.id, i18n.upload.wrong())

    if (len(logbook) > 0):
        # n = len(logbook)
        await bot.send_message(message.from_user.id, i18n.upload.found.qso(sum_qso=len(logbook)))
        data = []
        try:
            n = 0
            for i in range(len(logbook)):
                if ('prop_mode' in logbook[i] and 'sat_name' in logbook[i]):
                    if (logbook[i]['band'] == '13CM' and logbook[i]['prop_mode'] == 'SAT' and logbook[i]['sat_name'] == 'QO-100'):
                        qso_date = logbook[i].get('qso_date')[:4] + '-' + logbook[i].get('qso_date')[4:6] + '-' + logbook[i].get('qso_date')[6:]
                        time_on = logbook[i].get('time_on')[:2] + ':' + logbook[i].get('time_on')[2:4] + ':' + logbook[i].get('time_on')[4:6]
                        data.append([logbook[i].get('call'), logbook[i].get('band'), logbook[i].get('mode'), qso_date, time_on, logbook[i].get('prop_mode'), logbook[i].get('sat_name'), logbook[i].get('qsl_rcvd'), logbook[i].get('dxcc'), logbook[i].get('country'), logbook[i].get('gridsquare'), logbook[i].get('state'), logbook[i].get('cqz'), logbook[i].get('ituz'), logbook[i].get('operator')])
                        n += 1
        except:
            pass
        db.add_table_user(user)
        db.add_user_lotw_data(user+'_lotw', data)


        await bot.send_message(message.from_user.id, i18n.upload.db(n=n))
# ---------------------------------------------------------------------------------------------------

@router.callback_query(F.data == 'paper_qsl')
async def paper_qsl(callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, i18n.upload.paperqsl.title())
    await state.set_state(PaperQSLState.msg)

@router.message(StateFilter(PaperQSLState.msg))
async def paper_qsl_msg(message: types.Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = 'From ' + db.select_user_id(message.from_user.id)[1]


    if message.text is not None:
        if message.text == '/cancel':
           await state.clear()
           await message.reply(i18n.upload.cancel())
        else:
            await bot.send_message(537513849, user + '\n'+ message.text)

    elif message.photo is not None:
        await bot.send_photo(537513849, photo=message.photo[-1].file_id,
                             caption=user)

    elif message.document is not None:
        await bot.send_document(537513849, document=message.document.file_id,
                                caption=user)
    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.upload.paper.qsl2(), callback_data='paper_qsl')
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(1)
    await bot.send_message(message.from_user.id, i18n.upload.paper.ok(), reply_markup=kb.as_markup())