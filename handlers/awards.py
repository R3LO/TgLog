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

@router.callback_query(F.data == 'awards')
async def main_menu_awards(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    kb = InlineKeyboardBuilder()
    # W-QO100-R
    rus = len(db.get_stat_ru(user)) # количество RU
    rus_award_number =db.check_call_diplomas(user, 'w25r') # кортеж номер диплома
    if rus >= 25 and rus_award_number[0] != 0: # выполнен и получен
        kb.button(text=f'🏆 W-QO100-R # {rus_award_number[0]}', callback_data='dip_qo100_russia')
    elif rus >= 25 and rus_award_number[0] == 0: # выполнен и не получен
        kb.button(text=f'⭐️ W-QO100-R [{rus} ' + i18n.awards.of() + ' 25]', callback_data='dip_qo100_russia')
    elif rus < 25 and rus_award_number[0] == 0: # не выполнен и не получен
        kb.button(text=f'❌ W-QO100-R [{rus} ' + i18n.awards.of() + ' 25]', callback_data='dip_qo100_russia')
    elif rus < 25 and rus_award_number[0] != 0: # не выполнен и получен
        kb.button(text=f'🏆 W-QO100-R # {rus_award_number[0]}', callback_data='dip_qo100_russia')
    # W-QO100-C
    states = len(db.get_stat_states(user))
    states_award_number =db.check_call_diplomas(user, 'w100c') # кортеж номер диплома
    if states >= 100 and states_award_number[0] != 0: # выполнен и получен
        kb.button(text=f'🏆 W-QO100-С # {states_award_number[0]}', callback_data='dip_qo-100-countries')
    elif states >= 100 and states_award_number[0] == 0: # выполнен и не получен
        kb.button(text=f'⭐️ W-QO100-С [{states} ' + i18n.awards.of() + ' 100]', callback_data='dip_qo-100-countries')
    elif states < 100 and states_award_number[0] == 0: # не выполнен и не получен
        kb.button(text=f'❌ W-QO100-С [{states} ' + i18n.awards.of() + ' 100]', callback_data='dip_qo-100-countries')
    elif states < 100 and states_award_number[0] != 0: # не выполнен и получен
        kb.button(text=f'🏆 W-QO100-С # {states_award_number[0]}', callback_data='dip_qo-100-countries')
    # W-QO100-L
    locs = len(db.get_stat_loc(user))
    locs_award_number =db.check_call_diplomas(user, 'w100l') # кортеж номер диплома
    if locs >= 500 and locs_award_number[0] != 0: # выполнен и получен
        kb.button(text=f'🏆 W-QO100-L # {locs_award_number[0]}', callback_data='dip_qo-100-locators')
    elif locs >= 500 and locs_award_number[0] == 0: # выполнен и не получен
        kb.button(text=f'⭐️ W-QO100-L [{locs} ' + i18n.awards.of() + ' 500]', callback_data='dip_qo-100-locators')
    elif locs < 500 and locs_award_number[0] == 0: # не выполнен и не получен
        kb.button(text=f'❌ W-QO100-L [{locs} ' + i18n.awards.of() + ' 500]', callback_data='dip_qo-100-locators')
    elif locs < 500 and locs_award_number[0] != 0: # не выполнен и получен
        kb.button(text=f'🏆 W-QO100-L # {locs_award_number[0]}', callback_data='dip_qo-100-locators')
    # W-QO100-U
    unique = len(db.get_total_uniq_lotw(user))
    unique_award_number =db.check_call_diplomas(user, 'w1000u') # кортеж номер диплома
    if unique >= 1000 and unique_award_number[0] != 0: # выполнен и получен
        kb.button(text=f'🏆 W-QO100-U # {unique_award_number[0]}', callback_data='dip_qo-100-unique')
    elif unique >= 1000 and unique_award_number[0] == 0: # выполнен и не получен
        kb.button(text=f'⭐️ W-QO100-U [{unique} ' + i18n.awards.of() + ' 1000]', callback_data='dip_qo-100-unique')
    elif unique < 1000 and unique_award_number[0] == 0: # не выполнен и не получен
        kb.button(text=f'❌ W-QO100-U [{unique} ' + i18n.awards.of() + ' 1000]', callback_data='dip_qo-100-unique')
    elif unique < 1000 and unique_award_number[0] != 0: # не выполнен и получен
        kb.button(text=f'🏆 W-QO100-U # {unique_award_number[0]}', callback_data='dip_qo-100-unique')
    # W-QO100-B
    base = db.get_total_qso_log(user)[0][0]
    base_award_number =db.check_call_diplomas(user, 'w1000b') # кортеж номер диплома
    if base >= 1000 and base_award_number[0] != 0: # выполнен и получен
        kb.button(text=f'🏆 W-QO100-B # {base_award_number[0]}', callback_data='dip_qo-100-base')
    elif base >= 1000 and base_award_number[0] == 0: # выполнен и не получен
        kb.button(text=f'⭐️ W-QO100-B [{base} ' + i18n.awards.of() + ' 1000]', callback_data='dip_qo-100-base')
    elif base < 1000 and unique_award_number[0] == 0: # не выполнен и не получен
        kb.button(text=f'❌ W-QO100-B [{base} ' + i18n.awards.of() + ' 1000]', callback_data='dip_qo-100-base')
    elif base < 1000 and base_award_number[0] != 0: # не выполнен и получен
        kb.button(text=f'🏆 W-QO100-B # {base_award_number[0]}', callback_data='dip_qo-100-base')
    # back
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(2, 2, 2, 1)
    await bot.send_message(callback.from_user.id, i18n.awards.title(), reply_markup=kb.as_markup())

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'back_main_menu')
async def back_main_menu(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, i18n.main.menu(), reply_markup=interlinemenu(i18n))

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'dip_qo100_russia')
async def dip_qo100_russia(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    last_number = db.get_last_number_diplomas('w25r')[1]
    q_rus = len(db.get_stat_ru(user))
    kb = InlineKeyboardBuilder()
    if q_rus >= 25:
        kb.button(text=i18n.awards.pdf(), callback_data='get_pdf_w25r')
    kb.button(text=i18n.back(), callback_data='awards')
    kb.adjust(1)
    if q_rus < 25:
        await bot.send_message(callback.from_user.id, i18n.awards.no.diploma(diploma='W-QO100-R'), reply_markup=kb.as_markup())
    else:
        last_number += 1
        res =db.check_call_diplomas(user, 'w25r')
        if res[0] != 0: # есть в базе
            await bot.send_message(callback.from_user.id, i18n.awards.diploma(number=res[0], diploma='W-QO100-R'), reply_markup=kb.as_markup())
        else: # нет в базе
            db.add_call_diplomas(user, 'w25r', last_number)
            await bot.send_message(callback.from_user.id, i18n.awards.congrats(number=last_number, diploma='W-QO100-R'), reply_markup=kb.as_markup())

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'dip_qo-100-locators')
async def dip_qo100_locators(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    last_number = db.get_last_number_diplomas('w100l')[1]
    q_locators = len(db.get_stat_loc(user))
    kb = InlineKeyboardBuilder()
    if q_locators >= 500:
        kb.button(text=i18n.awards.pdf(), callback_data='get_pdf_w100l')
    kb.button(text=i18n.back(), callback_data='awards')
    kb.adjust(1)
    if q_locators < 500:
        await bot.send_message(callback.from_user.id, i18n.awards.no.diploma(diploma='W-QO100-L'), reply_markup=kb.as_markup())
    else:
        last_number += 1
        res =db.check_call_diplomas(user, 'w100l')
        if res[0] != 0: # есть в базе
            await bot.send_message(callback.from_user.id, i18n.awards.diploma(number=res[0], diploma='W-QO100-L'), reply_markup=kb.as_markup())
        else: # нет в базе
            db.add_call_diplomas(user, 'w100l', last_number)
            await bot.send_message(callback.from_user.id, i18n.awards.congrats(number=last_number, diploma='W-QO100-L'), reply_markup=kb.as_markup())

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'dip_qo-100-countries')
async def dip_qo100_countries(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    last_number = db.get_last_number_diplomas('w100c')[1]
    q_states = len(db.get_stat_states(user))
    kb = InlineKeyboardBuilder()
    if q_states >= 100:
        kb.button(text=i18n.awards.pdf(), callback_data='get_pdf_w100c')
    kb.button(text=i18n.back(), callback_data='awards')
    kb.adjust(1)
    if q_states < 100:
        await bot.send_message(callback.from_user.id, i18n.awards.no.diploma(diploma='W-QO100-C'), reply_markup=kb.as_markup())
    else:
        last_number += 1
        res =db.check_call_diplomas(user, 'w100c')
        if res[0] != 0: # есть в базе
            await bot.send_message(callback.from_user.id, i18n.awards.diploma(number=res[0], diploma='W-QO100-C'), reply_markup=kb.as_markup())
        else: # нет в базе
            db.add_call_diplomas(user, 'w100c', last_number)
            await bot.send_message(callback.from_user.id, i18n.awards.congrats(number=last_number, diploma='W-QO100-C'), reply_markup=kb.as_markup())


# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'dip_qo-100-unique')
async def dip_qo100_unique(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    last_number = db.get_last_number_diplomas('w1000u')[1]
    q_unique = len(db.get_total_uniq_lotw(user))
    kb = InlineKeyboardBuilder()
    if q_unique >= 1000:
        kb.button(text=i18n.awards.pdf(), callback_data='get_pdf_w100u')
    kb.button(text=i18n.back(), callback_data='awards')
    kb.adjust(1)
    if q_unique < 1000:
        await bot.send_message(callback.from_user.id, i18n.awards.no.diploma(diploma='W-QO100-U'), reply_markup=kb.as_markup())
    else:
        last_number += 1
        res =db.check_call_diplomas(user, 'w1000u')
        if res[0] != 0: # есть в базе
            await bot.send_message(callback.from_user.id, i18n.awards.diploma(number=res[0], diploma='W-QO100-U'), reply_markup=kb.as_markup())
        else: # нет в базе
            db.add_call_diplomas(user, 'w1000u', last_number)
            await bot.send_message(callback.from_user.id, i18n.awards.congrats(number=last_number, diploma='W-QO100-C'), reply_markup=kb.as_markup())

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'dip_qo-100-base')
async def dip_qo100_base(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    last_number = db.get_last_number_diplomas('w1000b')[1]
    q_qsos = db.get_total_qso_log(user)[0][0]
    kb = InlineKeyboardBuilder()
    if q_qsos >= 1000:
        kb.button(text=i18n.awards.pdf(), callback_data='get_pdf_w100b')
    kb.button(text=i18n.back(), callback_data='awards')
    kb.adjust(1)
    if q_qsos < 1000:
        await bot.send_message(callback.from_user.id, i18n.awards.no.diploma(diploma='W-QO100-B'), reply_markup=kb.as_markup())
    else:
        last_number += 1
        res =db.check_call_diplomas(user, 'w1000b')
        if res[0] != 0: # есть в базе
            await bot.send_message(callback.from_user.id, i18n.awards.diploma(number=res[0], diploma='W-QO100-B'), reply_markup=kb.as_markup())
        else: # нет в базе
            db.add_call_diplomas(user, 'w1000b', last_number)
            await bot.send_message(callback.from_user.id, i18n.awards.congrats(number=last_number, diploma='W-QO100-B'), reply_markup=kb.as_markup())

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'get_pdf_w25r')
async def pdf_w25r(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)
    res =db.check_call_diplomas(user[1], 'w25r')
    # print('user', user)
    # print('res', res)
    rus = len(db.get_stat_ru(user[1]))
    # print('rus', rus)
    create_w25r_pdf(user[1], user[2], res[0], rus, i18n)
    await bot.send_message(callback.from_user.id, text=i18n.awards.qrx())
    pdf = user[1] + '_w25r.pdf'
    document = FSInputFile(pdf)
    await bot.send_document(callback.from_user.id, document)
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='awards')
    kb.adjust(1)
    await bot.send_message(callback.from_user.id, text=i18n.pdf.congrats(), reply_markup=kb.as_markup())


@router.callback_query(F.data == 'get_pdf_w100b')
async def pdf_w100b(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)
    res =db.check_call_diplomas(user[1], 'w1000b')
    # print('user', user)
    # print('res', res)
    qsos = db.get_total_qso_log(user[1])[0][0]
    # print('qsos', qsos)
    create_w1000b_pdf(user[1], user[2], res[0], qsos, i18n)
    await bot.send_message(callback.from_user.id, text=i18n.awards.qrx())
    pdf = user[1] + '_w1000b.pdf'
    document = FSInputFile(pdf)
    await bot.send_document(callback.from_user.id, document)
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='awards')
    kb.adjust(1)
    await bot.send_message(callback.from_user.id, text=i18n.pdf.congrats(), reply_markup=kb.as_markup())


@router.callback_query(F.data == 'get_pdf_w100c')
async def pdf_w100c(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)
    res =db.check_call_diplomas(user[1], 'w100c')
    states = len(db.get_stat_states(user[1]))
    # print(res)
    create_w100c_pdf(user[1], user[2], res[0], states, i18n)
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, text=i18n.awards.qrx())
    pdf = user[1] + '_w100c.pdf'
    document = FSInputFile(pdf)
    await bot.send_document(callback.from_user.id, document)
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='awards')
    kb.adjust(1)
    await bot.send_message(callback.from_user.id, text=i18n.pdf.congrats(), reply_markup=kb.as_markup())



@router.callback_query(F.data == 'get_pdf_w100l')
async def pdf_w100l(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)
    res =db.check_call_diplomas(user[1], 'w100l')
    # print('user', user)
    # print('res', res)
    locators = len(db.get_stat_loc(user[1]))
    # print('locs', locators)
    create_w100l_pdf(user[1], user[2], res, locators, i18n)
    await bot.send_message(callback.from_user.id, text=i18n.awards.qrx())
    pdf = user[1] + '_w500l.pdf'
    document = FSInputFile(pdf)
    await bot.send_document(callback.from_user.id, document)
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='awards')
    kb.adjust(1)
    await bot.send_message(callback.from_user.id, text=i18n.pdf.congrats(), reply_markup=kb.as_markup())


@router.callback_query(F.data == 'get_pdf_w100u')
async def pdf_w100u(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)
    res =db.check_call_diplomas(user[1], 'w1000u')
    # print('user', user)
    # print('res', res)
    unique = len(db.get_total_uniq_lotw(user[1]))
    # print('unique', unique)
    create_w1000u_pdf(user[1], user[2], res[0], unique, i18n)
    await bot.send_message(callback.from_user.id, text=i18n.awards.qrx())
    pdf = user[1] + '_w1000u.pdf'
    document = FSInputFile(pdf)
    await bot.send_document(callback.from_user.id, document)
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='awards')
    kb.adjust(1)
    await bot.send_message(callback.from_user.id, text=i18n.pdf.congrats(), reply_markup=kb.as_markup())