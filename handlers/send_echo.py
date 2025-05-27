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
        if (len(q) != 0):
            msg = ''
            await bot.send_message(message.from_user.id, f'{user[1].upper()}: Поиск по логу <b>{message.text.upper()}</b> 🔎 <b>{len(q)}</b> QSO')
            for i in range(len(q)):
                if q[i][1] is None: loc = '----'
                else: loc = q[i][1][0:4]
                msg += '➡️ ' + q[i][0] + ' '
                msg += '🔔 ' + q[i][5] + ' '
                msg += '📝 ' + q[i][4] + ' '
                msg += '🌐 ' + loc[0:4] + ' '
                msg += '\n'
                # + ' 🌐 ' + loc + '</b> \n"◽️
                # + '</b> 🌐 <b>' + loc + '</b>📡<b>' + '</b> 🔔' + q[i][5] + '</i> \n'
                # await bot.send_message(message.from_user.id, f'<b>{q[i][0]}</b> <b>{q[i][1]}</b> <i>{q[i][2]} {q[i][3]} {q[i][4]} {q[i][5]}</i>')

                # print(qso['call'], qso['gridsquare'], qso['qso_date'], qso['time'], qso['mode'])
            await bot.send_message(message.from_user.id, msg)
        else:
            await bot.send_message(message.from_user.id, f'{user[1].upper()}: Поиск по логу <b>{message.text}</b> 🔎 ничего не найдено \nВсе что вводится в строке сообщение ищется в вашем загруженном логе по полю позывной и локатор. \nВозможно вы не загрузили лог или в вашем логе нет такого позывного или локатора. \nИли для запуска бота нужно выпонить команду /start \n')
    else:
        await bot.send_message(message.from_user.id, f'⚠️ Загрузку файлов необходимо делать через меню, выбрав какой тип лога загружается. Введите /start')

    # await bot.send_message(message.from_user.id, text='⁉️ Ничего не выбрано из меню. \n Для продолжения выберите действие', reply_markup=interlinemenu())
