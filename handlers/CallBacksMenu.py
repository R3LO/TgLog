from aiogram import Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from state.uload_log import Upload_logState
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
import os


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
        await bot.send_message(message.from_user.id, '👍 Дождитесь результата обработки...\n\n')
        await bot.send_message(message.from_user.id, '✅ Лог получен. Обработка QRX...\n\n')
        await adif(users[1], download_path, message, bot, state)

        # await state.clear()
        # await bot.send_message(message.from_user.id, 'Для продолжения выбирте действие', reply_markup=interlinemenu())


    else:
        await message.reply("⛔️ Загрузка лога отменена")
        await state.clear()
        await bot.send_message(message.from_user.id, 'Для продолжения выбирте действие', reply_markup=interlinemenu())




async def adif(table_db: str, log: str, message: Message, bot: Bot, state):
    f = open(log, 'r')
    try:
        log = f.read().upper()
    except:
        pass
    # db = Database(os.getenv('DATABASE_NAME'))

    if ('<EOH>' in log) and ('<QSO_DATE:' in log) and ('<TIME_ON:' in log) and ('<BAND:' in log) and ('CALL:' in log) and ('<EOR>' in log):
        await bot.send_message(message.from_user.id, '✅ ADIF теги в логе есть <i>(предварительная оценка)</i>...')
        # log = log.replace("<", " <")
        log = log.splitlines()
        print(len(log))

        await state.clear()
    else:
        await bot.send_message(message.from_user.id, '❌ Не найден како-то нужный тег.')
        await bot.send_message(message.from_user.id, '🤷 Попробуйте еще раз загрузить 📎 исправленный log или введите слово <b>отмена</b> для выходя из режима загрузки лога 👇')
