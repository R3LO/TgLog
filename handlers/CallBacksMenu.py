from aiogram import Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from state.uload_log import Upload_logState
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
import os
import re


# from aiogram.types import Message, FSInputFile


async def CallBaksMenu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if (callback.data == 'upload_log'):
        await callback.message.delete()
        await callback.message.answer(f'<b>Выбрано</b>: Загрузить лог')
        await callback.message.answer(f'💡 <i><b>ADIF файл должен содержать следующие теги:</b></i> \n'
                                        f'▫️QSO_DATE \n'
                                        f'▫️TIME_ON \n'
                                        f'▫️CALL \n'
                                        f'▫️MODE \n'
                                        f'▫️SUBMODE (необязательное поле для цифровых видов) \n'
                                        f'▫️BAND \n'
                                        f'▫️GRIDSQUARE \n'
                                        f'▫️MY_GRIDSQUARE \n\n'
                                        f'💾 <b>Для загрузки нажмите ниже 📎 и выбирте ваш файл ADIF лога для загрузки в систему.</b> \n\n'
                                        f'<i>Для отмены загружки отправьте текстовое сообшние <b>отмена</b></i>')
        await state.set_state(Upload_logState.upload_adif)


    elif (callback.data == 'search_log'):
        await callback.message.delete()
        await callback.message.answer('Поиск по логу')


async def upload_adif(message: types.Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if message.document:
        file = 'logs\\' + users[1] + '_' + str(message.from_user.id) +'.txt'
        download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        await message.bot.download(message.document, destination=download_path)
        await bot.send_message(message.from_user.id, '✅ Файл загружен. Дождитесь результата...\n\n')
        await bot.send_message(message.from_user.id, '✅ Файл получен. Обработка. QRX...\n\n')
        await adif(users[1], download_path, message, bot, state)
        await bot.send_message(message.from_user.id, '✅ Вышел из режима загрузки лога. \n\n')
        await state.clear()
        await bot.send_message(message.from_user.id, 'Для продолжения выбирте действие', reply_markup=interlinemenu())
    else:
        await message.reply("⛔️ Загрузка лога отменена.")
        await state.clear()
        await bot.send_message(message.from_user.id, 'Для продолжения выбирте действие', reply_markup=interlinemenu())




async def adif(table_db: str, log: str, message: Message, bot: Bot, state):
    logbook = []
    try:
        raw = re.split('<EOR>|<EOH>', open(log).read().upper(), flags=re.IGNORECASE)
    except:
        await bot.send_message(message.from_user.id, '❌ Это не файл ADIF лога')
        return
    n = 0
    try:
        for record in raw[1:-1]:
            qso = {}
            ADIF_REC_RE = re.compile(r'<(.*?):(\d+).*?>([^<\t\f\v]+)')
            tags = ADIF_REC_RE.findall(record)
            for tag in tags:
                qso[tag[0].lower()] = tag[2][:int(tag[1])]
                if (qso[tag[0].lower()] == 'MFSK'):
                    qso[tag[0].lower()] = 'FT4'
            n += 1
            logbook.append(qso)
    except:
        await bot.send_message(message.from_user.id, '❌ Не найдены ADIF теги.')
    if n > 0:
        await bot.send_message(message.from_user.id, f'✅ В фвйле <b>{n}</b> QSO. QRX...')
    else:
        await bot.send_message(message.from_user.id, '❌ В файле нет данных о QSO. Обработка завершена.')
        return

   