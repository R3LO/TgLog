from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext


from keyboards.inline_menu_kb import interlinemenu
# Создаем объекты инлайн-кнопок


async def create_raiting(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Создание рейтинга...', reply_markup=interlinemenu())
