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
from handlers.create_pdf import create_w100c_pdf, create_w100l_pdf, create_w1000b_pdf, create_w1000u_pdf, create_w25r_pdf
import sqlite3
import os

# Инициализируем роутер уровня модуля
router = Router()

@router.callback_query(F.data == 'log_info')
async def main_menu_log_info(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    kb.button(text='🌐 DXCC', callback_data='dxcc')
    kb.button(text='🗂 LOC', callback_data='loc')
    kb.button(text='🪙 CQ', callback_data='cq')
    kb.button(text='🪙 ITU', callback_data='itu')
    kb.button(text='🇷🇺 RUSSIA', callback_data='russia')
    kb.button(text='📗 Uniq Log', callback_data='ulog')
    kb.button(text='📘 Uniq LoTW', callback_data='ulotw')
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(4, 3)
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    try:
        total_qsos_log = db.get_total_qso_log(user)
        total_qsos_lotw = db.get_total_qso_lotw(user)
        qsos = total_qsos_log[0][0]
        lotws = total_qsos_lotw[0][0]
        dxcc =  db.get_stat_states(user)
        qra =  db.get_stat_loc(user)
        cqz =  db.get_stat_cqz(user)
        ituz =  db.get_stat_ituz(user)
        uniq_log = db.get_total_uniq_log(user)
        uniq_lotw = db.get_total_uniq_lotw(user)

        total_by_band = db.get_stat_bands(user)
        band_msg = '\n' + i18n.log.mode() + '\n'
        for i  in range(len(total_by_band)):
            band_msg += f'▫️ {total_by_band[i][0]} ▫️ {total_by_band[i][1]} ▫️ {total_by_band[i][2]} QSO\n'

        await bot.send_message(callback.from_user.id,
                    i18n.log.title(user=user) + '\n' +
                    f'{band_msg}\n' +
                    i18n.log.info1(qso=qsos, uqso=len(uniq_log)) + '\n\n' +
                    i18n.log.info2(lotws=lotws, uniq_lotw=len(uniq_lotw), percent= "{:,.2f}".format(lotws / qsos * 100)) + '\n\n' +
                    i18n.log.info3() + '\n' +
                    f'▫️LoTW DXCC:  <b>{len(dxcc)}</b> \n'
                    f'▫️LoTW QRA locators:  <b>{len(qra)}</b> \n'
                    f'▫️LoTW CQ zone:  <b>{len(cqz)}</b> \n'
                    f'▫️LoTW ITU zone:  <b>{len(ituz)}</b> \n'
                    , reply_markup=kb.as_markup()
                    )
    except:
        await bot.send_message(callback.from_user.id, 'Needs upload main log', reply_markup=kb.as_markup())



@router.callback_query(F.data == 'dxcc')
async def get_dxcc(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='log_info')
    try:
        stat_dxcc = db.get_stat_states(user)
        if len(stat_dxcc) != 0:
            msg = f'🏆 <b>{user}</b>: DXCC LoTW CFM 🛰 QO-100\n\n# ▫️ COUNTRY ▫️ CALLSIGN\n'
            for i in range(len(stat_dxcc)):
                msg += f'{i+1} ▫️ {stat_dxcc[i][0]}  ▫️  {stat_dxcc[i][1]}\n'
            await bot.send_message(callback.from_user.id,
                                f'{msg}\n ⭐️ Total DXCC: <b>{i+1}</b>'
                                , reply_markup=kb.as_markup()
                                )
        else:
            await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())
    except:
        await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())

@router.callback_query(F.data == 'loc')
async def get_loc(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='log_info')
    try:
        stat_loc = db.get_stat_loc(user)
        if len(stat_loc) != 0:
            file = 'logs/' + user + '_QRA.txt'
            upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
            txt = f'---=== {user}: ' + i18n.log.loc() + ' ===---\n\n'
            for i in range(len(stat_loc)):
                txt += f'{i+1}: {stat_loc[i][0]}  {stat_loc[i][1]}\n'
            with open(upload_path, 'w', encoding='utf-8') as f:
                f.write(txt)
            await bot.send_message(callback.from_user.id, text=i18n.loc.file())
            document = FSInputFile(upload_path)
            await bot.send_document(callback.from_user.id, document)
            await bot.send_message(callback.from_user.id,
                                f'⭐️ Total QRA loc: {len(stat_loc)}'
                                , reply_markup=kb.as_markup()
                                )
        else:
            await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())
    except:
        await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())

@router.callback_query(F.data == 'cq')
async def get_cq(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='log_info')
    try:
        stat_cqz = db.get_stat_cqz(user)
        if len(stat_cqz) != 0:
            msg = f'🏆 <b>CQ Zones LoTW CFM for {user} 🛰 QO-100</b>\n\nCQ ZONE ▫️ CALLSIGN\n'
            for i in range(len(stat_cqz)):
                msg += f'{stat_cqz[i][0]}   {stat_cqz[i][1]}\n'
            await bot.send_message(callback.from_user.id,
                                f'{msg}\n⭐️ Total CQ zones: <b>{i+1}</b>'
                                , reply_markup=kb.as_markup()
                                )
        else:
            await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())
    except:
        await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())

@router.callback_query(F.data == 'itu')
async def get_cq(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='log_info')
    try:
        stat_ituz = db.get_stat_ituz(user)
        if len(stat_ituz) != 0:
            msg = f'🏆 <b>ITU Zones LoTW CFM for {user}🛰 QO-100</b>\n\nITU ZONE ▫️ CALLSIGN\n'
            for i in range(len(stat_ituz)):
                msg += f'{stat_ituz[i][0]}   {stat_ituz[i][1]}\n'
            await bot.send_message(callback.from_user.id,
                                f'{msg}\n⭐️ Total ITU zones: <b>{i+1}</b>'
                                , reply_markup=kb.as_markup()
                                )
        else:
            await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())
    except:
        await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())


@router.callback_query(F.data == 'russia')
async def get_russia(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='log_info')
    try:
        if i18n.i18n.lang() == 'ru':
            stat_ru = db.get_stat_ruru(user)
        else:
            stat_ru = db.get_stat_ruen(user)
        if len(stat_ru) != 0:
            msg = i18n.log.rus(user=user) + '\n\n'
            for i in range(len(stat_ru)):
                msg += f'{i+1}:  {stat_ru[i][0]}  ▫️  {stat_ru[i][1]}\n'
            await bot.send_message(callback.from_user.id,
                                f'{msg}\n⭐️  ' + i18n.log.rus.total() + f' <b>{i+1}</b>'
                                , reply_markup=kb.as_markup()
                                )
        else:
            await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())
    except:
        await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())


@router.callback_query(F.data == 'ulog')
async def get_russia(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='log_info')
    try:
        uniq_log = db.get_total_uniq_log(user)
        if len(uniq_log) != 0:
            file = 'logs/' + user + '_uniq_log.txt'
            upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
            txt = f'---=== {user}: Unique Callsigns by main log ===---\n\n'
            for i in range(len(uniq_log)):
                txt += f'{i+1}:  {uniq_log[i][0]}  {uniq_log[i][1]}  {uniq_log[i][2]}   {uniq_log[i][3]}  {uniq_log[i][4]}\n'
            with open(upload_path, 'w', encoding='utf-8') as f:
                f.write(txt)
            await bot.send_message(callback.from_user.id, text=i18n.uniquelog.file())
            document = FSInputFile(upload_path)
            await bot.send_document(callback.from_user.id, document)
            await bot.send_message(callback.from_user.id,
                                f'⭐️ Total unique callsigns: <b>{len(uniq_log)}</b>'
                                , reply_markup=kb.as_markup()
                                )
        else:
            await bot.send_message(callback.from_user.id, i18n.log.need.log(), reply_markup=kb.as_markup())
    except:
        await bot.send_message(callback.from_user.id, i18n.log.need.log(), reply_markup=kb.as_markup())


@router.callback_query(F.data == 'ulotw')
async def get_russia(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='log_info')
    try:
        uniq_lotw = db.get_total_uniq_lotw(user)
        if len(uniq_lotw) != 0:
            file = 'logs/' + user + '_uniq_lotw.txt'
            upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
            txt = f'---=== {user}: Unique Callsigns according to LoTW ===---\n\n'
            for i in range(len(uniq_lotw)):
                txt += f'{i+1}:  {uniq_lotw[i][0]}  {uniq_lotw[i][1]}  {uniq_lotw[i][2]}   {uniq_lotw[i][3]}  {uniq_lotw[i][4]}\n'
            with open(upload_path, 'w', encoding='utf-8') as f:
                f.write(txt)
            await bot.send_message(callback.from_user.id, text=i18n.uniquelotw.file())
            document = FSInputFile(upload_path)
            await bot.send_document(callback.from_user.id, document)
            await bot.send_message(callback.from_user.id,
                                f'⭐️ Total unique LoTW callsigns: <b>{len(uniq_lotw)}</b>'
                                , reply_markup=kb.as_markup()
                                )
        else:
            await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())
    except:
        await bot.send_message(callback.from_user.id, i18n.log.need.lotw(), reply_markup=kb.as_markup())