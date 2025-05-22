from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
import asyncio
from dotenv import load_dotenv
import os
# from utils.commands import set_commands
from handlers.start import get_start
from handlers.register import start_register, register_call, register_name
from handlers.main_menu import main_menu
from handlers.admin.raiting import create_raiting
from handlers.CallBacksMenu import CallBaksMenu
from state.register import RegisterState
from filters.CheckAdmin import CheckAdmin


load_dotenv()

token = os.getenv('TOKEN')
admin_id = os.getenv('ADMIN_ID')

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def start_bot(bot):
    await bot.send_message(537513849, text='👌 Бот запущен...')

dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))

# Регистируем хендлеры регистрации
dp.message.register(start_register, F.text=='✅ РЕГИСТРАЦИЯ')
dp.message.register(main_menu, F.text=='☰ Меню')
dp.message.register(register_call, RegisterState.regCall)
dp.message.register(register_name, RegisterState.regName)
dp.message.register(create_raiting, Command(commands='raiting'), CheckAdmin())
dp.callback_query.register(CallBaksMenu)

async def start():
    # await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_upates=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())