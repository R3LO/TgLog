from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
import asyncio
from dotenv import load_dotenv
import os
from utils.commands import set_commands
from handlers.start import get_start, get_menu
from handlers.register import start_register, register_call, register_name
from handlers.my_profile import my_profile
from handlers.CallBacksMenu import upload_adif, upload_adif_lotw
from handlers.main_menu import main_menu
from handlers.send_echo import send_echo
from handlers.admin.raiting import create_raiting
from handlers.CallBacksMenu import CallBaksMenu
from state.register import RegisterState
from state.uload_log import Upload_logState
from state.upload_lotw import Upload_lotwState
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
dp.message.register(get_menu, Command(commands='menu'))

# Регистируем хендлеры регистрации
dp.message.register(start_register, F.text=='✅ РЕГИСТРАЦИЯ')
dp.message.register(my_profile, F.text=='💼 Мой профиль')
dp.message.register(main_menu, F.text=='☰ Меню')
dp.message.register(register_call, RegisterState.regCall)
dp.message.register(register_name, RegisterState.regName)
dp.message.register(upload_adif, Upload_logState.upload_adif)
dp.message.register(upload_adif_lotw, Upload_lotwState.upload_adif_lotw)
dp.message.register(send_echo)
dp.message.register(create_raiting, Command(commands='raiting'), CheckAdmin())
dp.callback_query.register(CallBaksMenu)

async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_upates=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())