from aiogram import Bot
from aiogram.types import Message
from keyboards.inline_menu_kb import interlinemenu
async def send_echo(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, text='⁉️ Ничего не выбрано из меню. \n Для продолжения выбирте действие', reply_markup=interlinemenu())