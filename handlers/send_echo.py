from aiogram import Bot
from aiogram.types import Message
from aiogram.types import ContentType
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
import os

async def send_echo(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)
    # print(message.text)
    if (user and message.text):
        if ('🌍' in message.text):
                loc = message.text[message.text.find('🌍'):].split()[1][0:4]
                await res_db(user[1].upper(), message, loc, bot)
        if ('FT4' in message.text or 'FT8' in message.text):
                call = message.text.split()[5]
                await res_db(user[1].upper(), message, call, bot)
        if ('CW' in message.text or 'SSB' in message.text or 'DIGI' in message.text):
                call = message.text.split()[3]
                await res_db(user[1].upper(), message, call, bot)
        if ('🌍' not in message.text and 'FT4' not in message.text and 'FT8' not in message.text and 'DIGI' not in message.text and 'CW' not in message.text and 'SSB' not in message.text):
            call = message.text
            await res_db(user[1].upper(), message, call, bot)
    else:
        await bot.send_message(message.from_user.id, f'⚠️ Начните рабюту с регистрации, кнопки МЕНЮ или с команды /start')

    # await bot.send_message(message.from_user.id, text='⁉️ Ничего не выбрано из меню. \n Для продолжения выберите действие', reply_markup=interlinemenu())


async def res_db(user: str, message: Message, m: str, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    q = db.search_qso_data(user.upper(), m.upper())
    # print(q)
    if (len(q) != 0):
        msg = ''
        results = 0
        for i in range(len(q)):
            date, call, band, mode, loc, qsl = q[i][0], q[i][1], q[i][2], q[i][3], q[i][4], q[i][5]
            date =  str(date)
            date = date[6:8] + '-' + date[4:6] + '-' + date[0:4]
            if loc is None: loc = '-'
            if qsl == 'N':
                qsl = ''
            else: qsl = ' [L]'
            msg += f'➡️ <b>{call}</b> ◽️ {date} ◽️ {band} ◽️ {mode} ◽️ <b>{loc}</b> <b>{qsl}</b> \n'
            results += 1

        await bot.send_message(message.from_user.id, f'{user.upper()}: Поиск по запросу <b>{m.upper()}</b> 🔎 <b>{results}</b> QSO\n<i>Лимит не более 80 строк.</i>')
        await bot.send_message(message.from_user.id, msg)
    else:
        await bot.send_message(message.from_user.id, f'{user.upper()}: Поиск по логу <b>{m}</b> 🔎 ничего не найдено \nВсе что вводится в строке сообщение ищется в вашем загруженном логе по полю позывной и локатор. \nВозможно вы не загрузили лог или в вашем логе нет такого позывного или локатора. \nИли для запуска бота нужно выпонить команду /start \n')
