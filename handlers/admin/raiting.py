from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext


from keyboards.menu_kb import main_menu
# Создаем объекты инлайн-кнопок


async def create_raiting(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Создание рейтинга...', reply_markup=main_menu())
    