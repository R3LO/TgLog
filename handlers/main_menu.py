from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
from utils.database import Database
from keyboards.inline_menu_kb import interlinemenu
import re
import os
import asyncio


async def main_menu(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await bot.send_message(message.from_user.id, f'📡 <b>ГЛАВНОЕ МЕНЮ</b>',reply_markup=interlinemenu())
    else:
        await bot.send_message(message.from_user.id, f'⚠️ Вам необходимо зарегистрироваться!')
