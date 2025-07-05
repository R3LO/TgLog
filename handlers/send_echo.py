from aiogram import Bot
from aiogram.types import Message
from aiogram.types import ContentType
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
from fluentogram import TranslatorRunner
from aiogram import Router

import os

router = Router()

@router.message()
async def send_echo(message: Message, i18n: TranslatorRunner, bot: Bot):

    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)
    if message.content_type == 'text':
        # print(message.text)
        if (user and message.text):
            if ('🌍' in message.text):
                    loc = message.text[message.text.find('🌍'):].split()[1][0:4]
                    await res_db(user[1].upper(), message, loc, i18n, bot)
            if ('FT4' in message.text or 'FT8' in message.text):
                    call = message.text.split()[5]
                    await res_db(user[1].upper(), message, call, i18n, bot)
            if ('CW' in message.text or 'SSB' in message.text or 'DIGI' in message.text):
                    call = message.text.split()[3]
                    await res_db(user[1].upper(), message, call, i18n, bot)
            if ('🌍' not in message.text and 'FT4' not in message.text and 'FT8' not in message.text and 'DIGI' not in message.text and 'CW' not in message.text and 'SSB' not in message.text):
                call = message.text
                await res_db(user[1].upper(), message, call, i18n, bot)
        else:
            await bot.send_message(message.from_user.id, f'⚠️ Run /start')
    else:
        await bot.send_message(message.from_user.id, i18n.wwrong(), reply_markup=interlinemenu(i18n))


async def res_db(user: str, message: Message, m: str, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    try:
        q = db.search_qso_data(user.upper(), m.upper())
        if (len(q) != 0):
            msg = ''
            results = 0
            for i in range(len(q)):
                date, time, call, band, mode, loc, qsl = q[i][0], q[i][1], q[i][2], q[i][3], q[i][4], q[i][5], q[i][6]
                date = date[8:10] + '-' + date[5:7] + '-' + date[0:4]
                if loc is None or loc == '': loc = '-'
                if qsl == 'N':
                    qsl = ''
                else: qsl = '[L]'
                # # msg += f'➡️ <b>{call}</b> ◽️ {date} ◽️ {band} ◽️ {mode} ◽️ <b>{loc}</b> <b>{qsl}</b>\n'
                if (await check_tlog(user, call, date, time, band, mode) == True):
                    tlog = '[T]'
                else:
                    tlog = ''
                msg += f'➡️ <b>{call}</b> ◽️ {date} ◽️ {mode} ◽️ <b>{loc}</b> <b>{qsl}</b><b>{tlog}</b>\n'
                results += 1

            await bot.send_message(message.from_user.id, f'{user.upper()}: ' + i18n.search.result(m=m.upper(), results=results))
            await bot.send_message(message.from_user.id, msg)
        else:
            await bot.send_message(message.from_user.id, f'{user.upper()}: ' + i18n.search.no.result(m=m))
    except:
        await bot.send_message(message.from_user.id, f'{user.upper()}: '  + i18n.search.no.result(m=m))

async def check_tlog(user, call, date, time, band, mode):
    db = Database(os.getenv('DATABASE_NAME'))
    chck_table = db.check_exist_table(call)
    if chck_table:
        return db.check_for_tlog(user, call, date, time, band, mode)
    else:
        return False