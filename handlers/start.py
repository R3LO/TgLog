from aiogram import Bot
from aiogram.types import Message
from keyboards.register_kb import register_keyboard
from keyboards.main_kb import main_kb
from utils.database import Database
import os

async def get_start(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await bot.send_message(message.from_user.id, f'Для продолжения выберие действие по кнопкам ниже 👇\n\n', reply_markup=main_kb)
    else:
        await bot.send_message(message.from_user.id, f'Здравствуйте! \n\n'
                            f'Данный бот является частью группы 📡 <b>QO-100-RUSSIA</b> \n'
                            f'Разработчик бота: <b>Владимир R3LO</b> \n\n'
                            f'Основные возможности бота: \n'
                            f'➡️ Ведение аппартаного журнала в телеграм боте \n'
                            f'➡️ Поиск QSO в загруженном логе \n'
                            f'➡️ Конвертация лога в разные форматы \n'
                            f'➡️ Синхронизировать свой лог с LoTW \n'
                            f'➡️ Получить свой лог в ADIF формате \n'
                            f'➡️ Получение электронных дипломов \n\n'
                            f'💡 Для доступа к своим данным необходимо пройти простую регистрацию, сообщив свой позывной и имя. Все загруженные данные остаются в вашем личном кабинете. Для регистрации нажимите на кнопку РЕГИСТРАЦИЯ 👇',
                            reply_markup=register_keyboard
)