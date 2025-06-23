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

@router.callback_query(F.data == 'wipe_log')
async def main_menu_wipe_log(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.wipe.mainlog(), callback_data='wipe-main'),
    kb.button(text=i18n.wipe.lotw(), callback_data='wipe-lotw')
    kb.button(text=i18n.wipe.all(), callback_data='wipe-all')
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(3, 1)
    await bot.send_message(callback.from_user.id,
                    i18n.wipe.title()
                    , reply_markup=kb.as_markup()
                    )

@router.callback_query(F.data == 'wipe-all')
async def wipe_all(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    db.delete_all_logs(user)
    await bot.send_message(callback.from_user.id, i18n.wipe.all.res(), reply_markup=kb.as_markup())

@router.callback_query(F.data == 'wipe-main')
async def wipe_main(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    db.delete_main_log(user)
    await bot.send_message(callback.from_user.id, i18n.wipe.main.res(), reply_markup=kb.as_markup())

@router.callback_query(F.data == 'wipe-lotw')
async def wipe_lotw(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    db.delete_lotw_log(user)
    await bot.send_message(callback.from_user.id, i18n.wipe.lotw.res(), reply_markup=kb.as_markup())