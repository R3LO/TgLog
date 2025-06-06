from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.types import Message
from keyboards.register_kb import register_keyboard
from keyboards.main_kb import main_kb
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
import os
import math

async def get_start(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await bot.send_message(message.from_user.id, f'Для продолжения выберие действие по кнопкам ниже 👇\n\n', reply_markup=interlinemenu())
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
        await bot.send_message(message.from_user.id,
                               f'Для поиска по логу введите в сообщение позывной или локатор. Или выберите действие из главного меню.\n\n'
                               f'<b>☰ ГЛАВНОЕ МЕНЮ</b> 👇 \n\n',
                               reply_markup=interlinemenu())
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

async def get_stat_ru(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    stat_ru = db.get_stat_ru(user)
    msg = f'🏆 <b>Районы России LoTW CFM for {user} только для 🛰 QO-100</b>\n\n👇 Районы России -- Позывной CFM\n\n'
    for i in range(len(stat_ru)):
        msg += f'{i+1}:  {stat_ru[i][0]}  -  {stat_ru[i][1]}\n'
    await bot.send_message(message.from_user.id,
                           f'{msg}\n 👍 Российских регионов: <b>{i+1}</b>'
                           )

async def get_cosmos(message: Message, bot: Bot):
    '''
    Выписка для длиплома Cosmos

    '''
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    cosmos_log = db.get_cosmos_uniq_log(user)
    file = 'logs/' + user + '_cosmos_log.csv'
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    txt = f''

    for i in range(len(cosmos_log)):
        if cosmos_log[i][0] is None:
            loc = 'None'
        else:
            loc = cosmos_log[i][0][0:4]
        txt += f'{i+1};{loc};{cosmos_log[i][1]};{cosmos_log[i][2]};{cosmos_log[i][3][0:5]};{cosmos_log[i][4][0:5]};{cosmos_log[i][5]};{cosmos_log[i][6]};{cosmos_log[i][7]}\n'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    await bot.send_message(message.from_user.id, text=
                        f'📌 <b>{user}</b> в завке на диплом Cosmos <b>{len(cosmos_log)}</b> уникальных позывных.\n\n'
                        f'💾 Файл выписки заявки на диплом Cosmos 👇 \n\n'
                        )
    document = FSInputFile(file_path)
    await bot.send_document(message.from_user.id, document)


async def get_uniq_log(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    uniq_log = db.get_total_uniq_log(user)
    file = 'logs/' + user + '_uniq_log.txt'
    upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    txt = f'---=== {user}: Список уникальных позывных из вашего лога ===---\n\n'
    for i in range(len(uniq_log)):
        txt += f'{i+1}:  {uniq_log[i][0]}  {uniq_log[i][1]}  {uniq_log[i][2]}   {uniq_log[i][3]}  {uniq_log[i][4]}\n'
    with open(upload_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    await bot.send_message(message.from_user.id, text=
                        f'📌 <b>{user}</b> в логе <b>{len(uniq_log)}</b> позывных уникальные.\n\n'
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
    txt = f'---=== {user}: Список уникальных позывных из LoTW ===---\n\n'
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
    txt = f'---=== {user}: подтвержденные QRA локаторы из LoTW ===---\n\n'
    for i in range(len(stat_loc)):
        txt += f'{i+1}: {stat_loc[i][0]}  {stat_loc[i][1]}\n'
    with open(upload_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    await bot.send_message(message.from_user.id, text=
                        f'📌 <b>{user}</b> у вас <b>{len(stat_loc)}</b> подтвержденных QRA локатора.\n\n'
                        f'💾 Файл со списом подтвержденных локторов ниже 👇 \n\n'
                        )
    document = FSInputFile(upload_path)
    await bot.send_document(message.from_user.id, document)
