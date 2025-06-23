from aiogram import Bot
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
from aiogram.types import FSInputFile
from aiogram.fsm.state import default_state
from state.conv_adif import Conv_AdifState
from handlers.create_pdf import create_w100c_pdf, create_w100l_pdf, create_w1000b_pdf, create_w1000u_pdf, create_w25r_pdf
import sqlite3
import os
import re
import asyncio

# Инициализируем роутер уровня модуля
router = Router()

@router.callback_query(F.data == 'conv_log')
async def main_menu_conv_log(callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    await callback.message.delete()
    await callback.message.answer(i18n.convert.title())
    await state.clear()
    await state.update_data(user=user)
    await state.set_state(Conv_AdifState.conv_adif)

@router.message(StateFilter(Conv_AdifState.conv_adif))
async def conv_adif(message: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user = data['user']
    if message.document:
        file = 'logs/' + user + '_' + str(message.from_user.id) +'_conv.adi'
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        await message.bot.download(message.document, destination=file_path)
        file_size = os.path.getsize(file_path)
        if (file_size > 10 * 1024 * 1024):
            await bot.send_message(message.from_user.id, i18n.convert.bigfile())
            await state.clear()
        await conv_adif_process(file_path, user, message, i18n, bot)
        await state.clear()
    else:
        await message.reply(i18n.convert.cancel())
        await state.clear()

async def conv_adif_process(file_log: str, user, message: Message, i18n: TranslatorRunner, bot: Bot):
    error = False
    file = 'logs/' + user + '_conv.adi'
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    logbook = []
    try:
        raw = re.split('<EOR>|<EOH>', open(file_log, encoding="utf8", errors='ignore').read().upper(), flags=re.IGNORECASE)
    except:
        await bot.send_message(message.from_user.id, i18n.convert.wrongfile())
        return
    try:
        for record in raw[1:-1]:
            if (':0><' in record): record = record.replace(':0><', ':1> <')
            qso = {}
            ADIF_REC_RE = re.compile(r'<(.*?):(\d+).*?>([^<\t\f\v]+)')
            tags = ADIF_REC_RE.findall(record)
            for tag in tags:
                qso[tag[0].lower()] = tag[2][:int(tag[1])]
            # if ('gridsquare' not in qso): qso['gridsquare'] = ' '
            logbook.append(qso)
    except:
        await bot.send_message(message.from_user.id, i18n.convert.wrongfile())

    if len(logbook) > 0:
        sum_qso = len(logbook)
        await bot.send_message(message.from_user.id, i18n.convert.uploaded(sum_qso=sum_qso))
        data = []
        with open(file_path, 'w') as f:
            str = f'TLog converter for {user}\n<EOH>\n'
            f.writelines(str)
            for i in range(len(logbook)):
                logbook[i]['prop_mode'] = 'SAT'
                logbook[i]['sat_name'] = 'QO-100'
                logbook[i]['band'] = '13CM'
                # logbook[i]['operator'] = user
                str = ''
                for key in logbook[i]:
                    str += f'<{key.upper()}:{len(logbook[i][key])}>{logbook[i][key].upper()} '
                str += '<EOR>\n'
                f.writelines(str)
        kb = InlineKeyboardBuilder()
        kb.button(text=i18n.back(), callback_data='main_menu')
        await bot.send_message(message.from_user.id, i18n.convert.ready())
        document = FSInputFile(file_path)
        await bot.send_document(message.from_user.id, document)
        await asyncio.sleep(3)
        await bot.send_message(message.from_user.id, i18n.main.menu(), reply_markup=interlinemenu(i18n))


    else:
        await bot.send_message(message.from_user.id, i18n.convert.wrongfile())
        return
