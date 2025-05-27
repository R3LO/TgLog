from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
from utils.database import Database
# from keyboards.menu_kb import main_menu
from keyboards.main_kb import main_kb
import re
import os
import asyncio


async def my_profile(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await bot.send_message(message.from_user.id, f'⚠️ Опция в разработке')
    else:
        await bot.send_message(message.from_user.id, f'❌ Необходимо зарегистрироваться. Нажмите /start')
