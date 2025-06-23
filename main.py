from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
import asyncio
from dotenv import load_dotenv
import os
from utils.commands import set_commands
from handlers.main_menu import main_menu
from handlers.send_echo import send_echo
from handlers.admin.raiting import create_raiting
from filters.CheckAdmin import CheckAdmin
from handlers import start, register
from handlers import ranking, awards, log_info, wipe_log, convert, download, upload, profile, send_echo, help, utilites
from fluentogram import TranslatorHub
from utils.i18n import create_translator_hub
from middlewares.i18n import TranslatorRunnerMiddleware

load_dotenv()

token = os.getenv('TOKEN')
admin_id = os.getenv('ADMIN_ID')

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def start_bot(bot):
    await bot.send_message(537513849, text='👌 Бот запущен...')


# Регистриуем роутеры в диспетчере
dp.include_router(start.router)
dp.include_router(upload.router)
dp.include_router(profile.router)
dp.include_router(convert.router)
dp.include_router(register.router)
dp.include_router(utilites.router)
dp.include_router(send_echo.router)
dp.include_router(download.router)
dp.include_router(wipe_log.router)
dp.include_router(log_info.router)
dp.include_router(awards.router)
dp.include_router(ranking.router)
dp.include_router(help.router)

# Создаем объект типа TranslatorHub
translator_hub: TranslatorHub = create_translator_hub()

# Регистрируем миддлварь для i18n
dp.update.middleware(TranslatorRunnerMiddleware())

dp.startup.register(start_bot)


async def start():
    await set_commands(bot)
    try:
        # await dp.start_polling(bot, skip_upates=True)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, _translator_hub=translator_hub)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())