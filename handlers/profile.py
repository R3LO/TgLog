from aiogram import Bot
from aiogram.types import Message
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, StateFilter
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from aiogram.utils.keyboard import InlineKeyboardBuilder
from state.register import ProfileEditState
from aiogram.types import FSInputFile
from aiogram.fsm.state import default_state
from handlers.create_pdf import create_w100c_pdf, create_w100l_pdf, create_w1000b_pdf, create_w1000u_pdf, create_w25r_pdf
import sqlite3
import os

# Инициализируем роутер уровня модуля
router = Router()

@router.callback_query(F.data == 'profile')
async def main_menu_profile(callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.profile.change.name(), callback_data='edit_name')
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(2)
    rus_award_number = db.check_call_diplomas(user[1], 'w25r')[0]
    if (rus_award_number == 0):
        rus_award_number = i18n.profile.status.diploma()
    else:
        rus_award_number = ' #' + str(rus_award_number)
    states_award_number = db.check_call_diplomas(user[1], 'w100c')[0]
    if (states_award_number == 0):
        states_award_number = i18n.profile.status.diploma()
    else:
        states_award_number = ' #' + str(states_award_number)
    locs_award_number =db.check_call_diplomas(user[1], 'w100l')[0]
    if (locs_award_number == 0):
        locs_award_number = i18n.profile.status.diploma()
    else:
        locs_award_number = ' #' + str(locs_award_number)
    unique_award_number =db.check_call_diplomas(user[1], 'w1000u')[0]
    if (unique_award_number == 0):
        unique_award_number = i18n.profile.status.diploma()
    else:
        unique_award_number = ' #' + str(unique_award_number)
    base_award_number =db.check_call_diplomas(user[0], 'w1000b')[0]
    if (base_award_number == 0):
        base_award_number = i18n.profile.status.diploma()
    else:
        base_award_number = ' #' + str(base_award_number)
    await bot.send_message(callback.from_user.id, i18n.profile.data(user1=user[1], user2=user[2], rus_award_number=rus_award_number, states_award_number=states_award_number, locs_award_number=locs_award_number, unique_award_number=unique_award_number, base_award_number=base_award_number)
                           , reply_markup=kb.as_markup())

@router.callback_query(F.data == 'edit_name')
async def main_menu_profile(callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    await bot.send_message(callback.from_user.id, i18n.profile.name())
    await state.set_state(ProfileEditState.editName)

@router.message(StateFilter(ProfileEditState.editName), F.text.isalpha())
async def edit_name(message: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    await state.update_data(name=message.text)
    data = await state.get_data()
    name = data['name']
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='profile')
    await bot.send_message(message.from_user.id, i18n.profile.change(user=user, name=name), reply_markup=kb.as_markup())
    db.edit_user(user, name)
    await state.clear()

@router.message(StateFilter(ProfileEditState.editName))
async def edit_name(message: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, i18n.profile.no.name())