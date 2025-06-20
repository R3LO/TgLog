from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
import asyncio
from dotenv import load_dotenv
import os
from utils.commands import set_commands
# from handlers.start import get_start, get_menu, get_stat_states, get_stat_loc, get_stat_cqz, get_stat_ituz, get_uniq_log, get_uniq_lotw, get_cosmos, get_stat_ru
# from handlers.register import start_register, register_call, register_name
# from handlers.my_profile import my_profile
# from handlers.CallBacksMenu import upload_adif, upload_adif_lotw, conv_adif
from handlers.main_menu import main_menu
from handlers.send_echo import send_echo
from handlers.admin.raiting import create_raiting
# from handlers.CallBacksMenu import CallBaksMenu
from state.register import RegisterState
# from state.uload_log import Upload_logState
from state.upload_lotw import Upload_lotwState
from state.conv_adif import Conv_AdifState
from filters.CheckAdmin import CheckAdmin
# from create_dp import dp
from handlers import start, register
from handlers import ranking, awards, log_info
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
dp.include_router(register.router)
dp.include_router(log_info.router)
dp.include_router(awards.router)
dp.include_router(ranking.router)

# Создаем объект типа TranslatorHub
translator_hub: TranslatorHub = create_translator_hub()

# Регистрируем миддлварь для i18n
dp.update.middleware(TranslatorRunnerMiddleware())


dp.startup.register(start_bot)
# dp.message.register(get_start, Command(commands='start'))
# dp.message.register(get_menu, Command(commands='menu'))
# dp.message.register(get_stat_states, Command(commands='stat_states'))
# dp.message.register(get_stat_loc, Command(commands='stat_loc'))
# dp.message.register(get_stat_cqz, Command(commands='stat_cqz'))
# dp.message.register(get_stat_ituz, Command(commands='stat_ituz'))
# dp.message.register(get_uniq_log, Command(commands='uniq_log'))
# dp.message.register(get_uniq_lotw, Command(commands='uniq_lotw'))
# dp.message.register(get_cosmos, Command(commands='cosmos'))
# dp.message.register(get_stat_ru, Command(commands='stat_ru'))

# # Регистируем хендлеры регистрации
# dp.message.register(start_register, F.text=='✅ РЕГИСТРАЦИЯ')
# dp.message.register(my_profile, F.text=='💼 Мой профиль')
# dp.message.register(main_menu, F.text=='☰ Меню')
# dp.message.register(register_call, RegisterState.regCall)
# dp.message.register(register_name, RegisterState.regName)
# dp.message.register(upload_adif, Upload_logState.upload_adif)
# dp.message.register(upload_adif_lotw, Upload_lotwState.upload_adif_lotw)
# dp.message.register(conv_adif, Conv_AdifState.conv_adif)
# dp.message.register(send_echo)
# dp.message.register(create_raiting, Command(commands='raiting'), CheckAdmin())
# dp.callback_query.register(CallBaksMenu)



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