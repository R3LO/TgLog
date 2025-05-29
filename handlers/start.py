from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.types import Message
from keyboards.register_kb import register_keyboard
from keyboards.main_kb import main_kb
from utils.database import Database
import os
import math

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


async def get_menu(message: Message, bot: Bot):
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

async def get_stat_states(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    stat_dxcc = db.get_stat_states(user)
    msg = f'🏆 <b>DXCC LoTW CFM for {user} только для 🛰 QO-100</b>\n(NN -- COUNTRY -- CALLSIGN -- CFM QSOs)\n'
    for i in range(len(stat_dxcc)):
        msg += f'{i+1}   {stat_dxcc[i][0]}   {stat_dxcc[i][1]}    {stat_dxcc[i][2]}\n'
    await bot.send_message(message.from_user.id,
                           f'{msg}\n 👍 ВСЕГО CFM DXCC: <b>{i+1}</b>'
                           )

async def get_stat_cqz(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    stat_cqz = db.get_stat_cqz(user)
    msg = f'🏆 <b>CQ Zones LoTW CFM for {user} только для 🛰 QO-100</b>\n(CQ ZONE -- CALLSIGN)\n'
    for i in range(len(stat_cqz)):
        msg += f'{stat_cqz[i][0]}   {stat_cqz[i][1]}\n'
    await bot.send_message(message.from_user.id,
                           f'{msg}\n 👍 ВСЕГО CQ зон: <b>{i+1}</b>'
                           )

async def get_stat_ituz(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    stat_ituz = db.get_stat_ituz(user)
    msg = f'🏆 <b>ITU Zones LoTW CFM for {user} только для 🛰 QO-100</b>\n(ITU ZONE -- CALLSIGN)\n'
    for i in range(len(stat_ituz)):
        msg += f'{stat_ituz[i][0]}   {stat_ituz[i][1]}\n'
    await bot.send_message(message.from_user.id,
                           f'{msg}\n 👍 ВСЕГО ITU зон: <b>{i+1}</b>'
                           )

async def get_uniq_log(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    uniq_log = db.get_total_uniq_log(user)
    file = 'logs/' + user + '_uniq_log.txt'
    upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    txt = f'---=== {user}: Список уникальных позывныз из вашего лога ===---\n\n'
    for i in range(len(uniq_log)):
        txt += f'{i+1}:  {uniq_log[i][0]}  {uniq_log[i][1]}  {uniq_log[i][2]}   {uniq_log[i][3]}  {uniq_log[i][4]}\n'
    with open(upload_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    await bot.send_message(message.from_user.id, text=
                        f'📌 <b>{user}</b> в логе <b>{len(uniq_log)}</b> позывных юникальные.\n\n'
                        f'💾 Файл со списом уникальных позывных ниже 👇 \n\n'
                        )
    document = FSInputFile(upload_path)
    await bot.send_document(message.from_user.id, document)


async def get_uniq_lotw(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    uniq_lotw = db.get_total_uniq_lotw(user)
    file = 'logs/' + user + '_uniq_lotw.txt'
    upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    txt = f'---=== {user}: Список уникальных позывныз из LoTW ===---\n\n'
    for i in range(len(uniq_lotw)):
        txt += f'{i+1}:  {uniq_lotw[i][0]}  {uniq_lotw[i][1]}  {uniq_lotw[i][2]}   {uniq_lotw[i][3]}  {uniq_lotw[i][4]}\n'
    with open(upload_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    await bot.send_message(message.from_user.id, text=
                        f'📌 <b>{user}</b> в логе <b>{len(uniq_lotw)}</b> позывных из LoTW уникальные.\n\n'
                        f'💾 Файл со списом уникальных позывных ниже 👇 \n\n'
                        )
    document = FSInputFile(upload_path)
    await bot.send_document(message.from_user.id, document)


async def get_stat_loc(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    stat_loc = db.get_stat_loc(user)
    file = 'logs/' + user + '_QRA.txt'
    upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    txt = f'---=== {user}: подтверженные QRA локаторы из LoTW ===---\n\n'
    for i in range(len(stat_loc)):
        txt += f'{i+1}: {stat_loc[i][0]}  {stat_loc[i][1]}\n'
    with open(upload_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    await bot.send_message(message.from_user.id, text=
                        f'📌 <b>{user}</b> у вас <b>{len(stat_loc)}</b> подтверженных QRA локатора.\n\n'
                        f'💾 Файл со списом подтверденных локторов ниже 👇 \n\n'
                        )
    document = FSInputFile(upload_path)
    await bot.send_document(message.from_user.id, document)

    # db = Database(os.getenv('DATABASE_NAME'))
    # user = db.select_user_id(message.from_user.id)[1]
    # page = 0
    # stat_loc = db.get_stat_loc(user)
    # start_offset = page * 50
    # end_offset = start_offset + 50
    # msg = ''
    # n = 0
    # for i in range(math.ceil(len(stat_loc)/50)):
    #     print(f'{math.ceil(len(stat_loc)/50)} длина {len(stat_loc)/50}')
    #     for j in range(50):
    #         print(f'n = {n} = {len(stat_loc)} ДОБАВИЛИ')
    #         try:
    #             msg += f'{n+1}  ◽️ {stat_loc[n][0]}  ◽️ {stat_loc[n][1]}\n'
    #             print(f'{msg} \n')
    #         except:
    #             await bot.send_message(message.from_user.id, text=f'{msg} \n')
    #             return
    #         if j == 49 and n < len(stat_loc):
    #             print(f'n = {n} ВЫВЕЛИ')
    #             await bot.send_message(message.from_user.id, text=f'{msg} \n')
    #             msg = ''
    #         n += 1
