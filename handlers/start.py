from aiogram import Bot
from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram import Router
from aiogram.types import FSInputFile
from aiogram.types import Message
# from keyboards.register_kb import register_keyboard
# from keyboards.main_kb import main_kb
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
from fluentogram import TranslatorRunner
from aiogram.utils.keyboard import InlineKeyboardBuilder
# from create_dp import dp
import os
import math
from keyboards.inline_menu_kb import main_menu

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
@router.message(Command(commands=['start', 'menu']))
async def process_start_command(message: Message, i18n: TranslatorRunner, bot: Bot):
    await message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        # print(users)
        if users[5] == 'N':
            await bot.send_message(message.from_user.id, text=i18n.main.menu(), reply_markup=interlinemenu(i18n))
        else:
            await bot.send_message(message.from_user.id, text='🔎 Please wait...')
    else:
        kb = InlineKeyboardBuilder()
        kb.button(text=i18n.registration.button(), callback_data='new_user_registration')
        await bot.send_message(message.from_user.id, text=i18n.hello.new.user(), reply_markup = kb.as_markup())



# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='help')
