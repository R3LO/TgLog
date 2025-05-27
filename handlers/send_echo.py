from aiogram import Bot
from aiogram.types import Message
from aiogram.types import ContentType
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
import os

async def send_echo(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)
    if (user and message.text):
        q = db.search_qso_data(user[1].upper(), message.text.upper())
        # print(q)

        if (len(q) != 0):
            msg = ''
            results = 0
            for i in range(len(q)):
                call, band, mode, loc, qsl, qso = q[i][0], q[i][1], q[i][2], q[i][3], q[i][4], q[i][5]
                if loc is None: loc = 'no loc'
                if qsl == 'N':
                    qsl = ''
                else: qsl = 'LoTW CFM'
                msg += f'➡️ <b>{call}</b> ◽️ {band} ◽️ {mode} ◽️ <b>{loc}</b> ◽️ <b>{qsl}</b> <i>QSO({qso})</i>\n'
                results += qso

            await bot.send_message(message.from_user.id, f'{user[1].upper()}: Поиск по запросу <b>{message.text.upper()}</b> 🔎 <b>{results}</b> QSO')
            await bot.send_message(message.from_user.id, msg)
        else:
            await bot.send_message(message.from_user.id, f'{user[1].upper()}: Поиск по логу <b>{message.text}</b> 🔎 ничего не найдено \nВсе что вводится в строке сообщение ищется в вашем загруженном логе по полю позывной и локатор. \nВозможно вы не загрузили лог или в вашем логе нет такого позывного или локатора. \nИли для запуска бота нужно выпонить команду /start \n')
    else:
        await bot.send_message(message.from_user.id, f'⚠️ Начните рабюту с регистрации, кнопки МЕНЮ или с команды /start')

    # await bot.send_message(message.from_user.id, text='⁉️ Ничего не выбрано из меню. \n Для продолжения выберите действие', reply_markup=interlinemenu())
