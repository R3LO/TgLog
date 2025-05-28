from aiogram import Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from state.uload_log import Upload_logState
from state.upload_lotw import Upload_lotwState
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
import os
import re


# from aiogram.types import Message, FSInputFile


async def CallBaksMenu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)

    if (user):
        if (callback.data == 'upload_lotw'):
            await callback.message.delete()
            await callback.message.answer(f'<b>Выбрано</b>: Снхронизация лога с файлом из LoTW')
            await bot.send_message(callback.from_user.id,
                                   f'💡 <b>Для предотвращения \"утечек\" логина и пароля мы не запрашиваем данные сервиса LoTW, как это делают другие сервисы. Необходимый файл <b>lotwreport.adi</b> необходимо самостоятельно скачать из своей личной учетной записи LoTW.</b> \n\n'
                                   f'1️⃣ Войдите в свою учетную запись LoTW \n'
                                   f'2️⃣ Перейдите в <b>Your QSOs</b> \n'
                                   f'3️⃣ Перейдите в <b>Download Report</b> \n'
                                   f'4️⃣ Поставьте галочки <b>Include QSL details</b> и вторая галочка на <b>Include QSO station details (\"my\" station location fields)</b> \n'
                                   f'5️⃣ Нажмите <b>Download Report</b> и сохрание файл себе на диск \n'
                                   f'6️⃣ Загрузите скачанный файл сообщением нажав на 📎 \n\n'
                                   f'<i>Для отмены загрузки отправьте текстовым сообшнием слово <b>отмена</b></i>')
            await state.clear()
            await state.set_state(Upload_lotwState.upload_adif_lotw.state)


        if (callback.data == 'download_log'):
            await bot.send_message(callback.from_user.id, f'⚠️ Скачать весь лог в стадии тестирования')
        if (callback.data == 'full_search'):
            await bot.send_message(callback.from_user.id, f'⚠️ Полный поиск по логу в стадии тестирования')
        if (callback.data == 'qo100_log'):
            await bot.send_message(callback.from_user.id, f'⚠️ Конвертер в стадии тестирования')
        if (callback.data == 'my_diploma'):
            await bot.send_message(callback.from_user.id, f'⚠️ Выдача дипломов в стадии тестирования')

        if (callback.data == 'statistics'):
            await bot.send_message(callback.from_user.id, f'⚠️ Статистика в стадии тестирования')

        if (callback.data == 'help'):
            await bot.send_message(callback.from_user.id, f'⚠️ Помощь в стадии тестирования')


        if (callback.data == 'upload_log'):
            await callback.message.delete()
            await callback.message.answer(f'<b>Выбрано</b>: Загрузить лог')
            await callback.message.answer(f'💡 <i><b>Загружаемый ADIF файл доллжен быть размером не более <b>10Мб</b> и должен содержать обязательные теги:</b></i> \n'
                                            f'▫️QSO_DATE - дата QSO\n'
                                            f'▫️TIME_ON - время начало QSO\n'
                                            f'▫️CALL - позывной корреспондента\n'
                                            f'▫️MODE - вид связи\n'
                                            f'▫️SUBMODE - подвид связи, необязательное поле для цифровых видов \n'
                                            f'▫️<b>BAND - диапазон должен быть указан как 13CM</b>\n'
                                            f'▫️GRIDSQUARE - локатор корреспондента\n\n'
                                            f'💾 <b>Чтобы приступить к загрузке нажмите на 📎 ниже, выберите файл ADIF для загрузки.</b> \n\n'
                                            f'<i>Для отмены загрузки отправьте текстовым сообшнием слово <b>отмена</b></i>')
            await state.clear()
            await state.set_state(Upload_logState.upload_adif)



        # elif (callback.data == 'search_log'):
        #     await callback.message.delete()
        #     await callback.message.answer('Поиск по логу')
    else:
        await bot.send_message(callback.from_user.id, f'⚠️ Вам необходимо зарегистрироваться! Введите /start')

async def upload_adif_lotw(message: types.Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if message.document:
        file = 'logs/' + users[1] + '_' + str(message.from_user.id) +'_lotw.txt'
        download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        await message.bot.download(message.document, destination=download_path)
        file_size = os.path.getsize(download_path)
        if (file_size > 12 * 1024 * 1024):
            await bot.send_message(message.from_user.id, '⛔️ Размер файла очень большой.\n\n')
            await state.clear()
            await bot.send_message(message.from_user.id, 'Для продолжения выберите действие', reply_markup=interlinemenu())
            return
        await lotw(users[1], download_path, message, bot, state)
        await state.clear()
        await bot.send_message(message.from_user.id, '💡 <i>Вы можете начать пользоваться поиском по логу. Если сейчас в сообщением отправить мне часть позывного или локатора, то произойдет поиск по вашему логу по полю позывной или локатор.</i> \n\n Либо для продолжения выберите действие из меню.', reply_markup=interlinemenu())
    else:
        await message.reply("⛔️ Загрузка файла отменена.")
        await state.clear()
        await bot.send_message(message.from_user.id, 'Для продолжения выберите действие', reply_markup=interlinemenu())


async def upload_adif(message: types.Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if message.document:
        file = 'logs/' + users[1] + '_' + str(message.from_user.id) +'.txt'
        download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        await message.bot.download(message.document, destination=download_path)
        file_size = os.path.getsize(download_path)
        if (file_size > 10 * 1024 * 1024):
            await bot.send_message(message.from_user.id, '⛔️ Размер файла очень большой.\n\n')
            await state.clear()
            await bot.send_message(message.from_user.id, 'Для продолжения выберите действие', reply_markup=interlinemenu())
            return
        # await bot.send_message(message.from_user.id, f'✅ Файл размером <b>{round(file_size/1024, 2)}</b>Кб загружен. QRX...')
        # await bot.send_message(message.from_user.id, '✅ Началась обработка. QRX...')
        await adif(users[1], download_path, message, bot, state)
        # await bot.send_message(message.from_user.id, '✅ Вышел из режима загрузки лога. \n\n')
        await state.clear()
        await bot.send_message(message.from_user.id, '💡 <i>Вы можете начать пользоваться поиском по логу. Если сейчас в сообщением отправить мне часть позывного или локатора, то произойдет поиск по вашему логу по полю позывной или локатор.</i> \n\n Либо для продолжения выберите действие из меню.', reply_markup=interlinemenu())
    else:
        await message.reply("⛔️ Загрузка файла отменена.")
        await state.clear()
        await bot.send_message(message.from_user.id, 'Для продолжения выберите действие', reply_markup=interlinemenu())



async def lotw(table_db: str, log: str, message: Message, bot: Bot, state):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)
    logbook = []
    # try:
    #     with open(log, 'r') as f:
    #         raw = f.read()
    #         # print(raw)
    #         raw = re.split('<eor>|<eoh>')
    raw = re.split('<EOR>|<EOH>', open(log, encoding="utf8", errors='ignore').read().upper(), flags=re.IGNORECASE)
    # except:
    #     await bot.send_message(message.from_user.id, '❌ Это не файл из LoTW')
    #     return
    n = 0
    if (raw[0].split('\n')[0] == 'ARRL LOGBOOK OF THE WORLD STATUS REPORT'):
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
                if ('gridsquare' not in qso): qso['gridsquare'] = None
                logbook.append(qso)
        except:
            await bot.send_message(message.from_user.id, '❌ Не найдены ADIF теги.')
    else:
        await bot.send_message(message.from_user.id, '❌ Загруженный файл не с сайта ARRL LoTW')

    if n > 0:
        await bot.send_message(message.from_user.id, f'✅ В файле <b>{n}</b> LoTW QSL. QRX...')
        data = []
        try:
            for i in range(len(logbook)):
                if ('prop_mode' in logbook[i] and 'sat_name' in logbook[i]):
                    if (logbook[i]['band'] == '13CM' and logbook[i]['prop_mode'] == 'SAT' and logbook[i]['sat_name'] == 'QO-100'):
                        data.append([logbook[i].get('call'), logbook[i].get('band'), logbook[i].get('mode'), logbook[i].get('qso_date'), logbook[i].get('time_on'), logbook[i].get('prop_mode'), logbook[i].get('sat_name'), logbook[i].get('qsl_rcvd'), logbook[i].get('dxcc'), logbook[i].get('country'), logbook[i].get('gridsquare'), logbook[i].get('cqz'), logbook[i].get('ituz')])
            db.add_table_user(user[1])
            db.add_user_lotw_data(user[1]+'_lotw', data)
        except:
            pass


        await bot.send_message(message.from_user.id, f'✅ Данные LoTW отправлены в базу данных')





async def adif(table_db: str, log: str, message: Message, bot: Bot, state):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)
    error = False
    file = 'logs/' + user[1] + '_bad_log.txt'
    upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(upload_path, 'w'):   pass
    logbook = []
    try:
        raw = re.split('<EOR>|<EOH>', open(log, encoding="utf8", errors='ignore').read().upper(), flags=re.IGNORECASE)
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
            if ('gridsquare' not in qso): qso['gridsquare'] = None
            logbook.append(qso)
    except:
        await bot.send_message(message.from_user.id, '❌ Не найдены ADIF теги.')
    if n > 0:
        await bot.send_message(message.from_user.id, f'✅ В файле <b>{n}</b> QSO. QRX...')
        data = []
        for i in range(len(logbook)):
            if (logbook[i].get('call') is not None) and (logbook[i].get('qso_date') is not None) and (logbook[i].get('time_on') is not None) and (logbook[i].get('band') is not None) and (logbook[i].get('mode') is not None):
                data.append([logbook[i].get('call'), logbook[i].get('qso_date'), logbook[i].get('time_on'), logbook[i].get('band'), logbook[i].get('mode'), logbook[i].get('gridsquare')])

            else:
                error = True
                txt = '---=== Нет полных данных о QSO ===---\n' + '; '.join([f'{key.capitalize()}: {value}' for key, value in logbook[i].items()]) + '\n\n'
                with open(upload_path, 'a', encoding='utf-8') as f:
                    f.write(txt)


        db.add_table_user(user[1])
        db.add_user_qso_data(user[1], data)
        await bot.send_message(message.from_user.id, f'✅ Данные отправлены в базу данных')
        if error:
            await bot.send_message(message.from_user.id, f'❌ <b>При обработке файла возникли ошибки.</b> \n\n 💾 <i>Данные, которые не попали в базу, в прикрепленном файле ниже 👇</i>')
            document = FSInputFile(upload_path)
            await bot.send_document(message.from_user.id, document)


    else:
        await bot.send_message(message.from_user.id, '❌ В файле нет данных о QSO. Обработка завершена.')
        return
