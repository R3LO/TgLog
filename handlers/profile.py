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
    kb.button(text='✏️ Редактировать имя', callback_data='edit_name')
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(2)
    await bot.send_message(callback.from_user.id,
                           f'💼 <b>Ваши данные</b>\n\n'
                           f'📡 Позывной: <b>{user[1]}</b>\n'
                           f'👤 Имя и Фамилия: <b>{user[2]}</b>\n\n'
                           f'💡 <i>Позывной, имя и фамилия указываются на выдаваемых дипломах. Изменить можно только имя, для смены позывного обратитесь к администратору.</i>\n\n'
                           , reply_markup=kb.as_markup())

@router.callback_query(F.data == 'edit_name')
async def main_menu_profile(callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    await bot.send_message(callback.from_user.id, 'Введие ваше имя и фамилию')
    await state.set_state(ProfileEditState.editName)

@router.message(StateFilter(ProfileEditState.editName), F.text.isalpha())
async def edit_name(message: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    await state.update_data(name=message.text)
    data = await state.get_data()
    name = data['name']
    await bot.send_message(message.from_user.id, f'fff {user} {name}')
    db.edit_user(user, name)
    await state.clear()

@router.message(StateFilter(ProfileEditState.editName))
async def edit_name(message: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Это не имя')