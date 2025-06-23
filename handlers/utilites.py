# -*- coding: UTF-8 -*-
from aiogram import Bot, types
from aiogram.types import Message
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, StateFilter
from state.register import RegisterState
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from aiogram.utils.keyboard import InlineKeyboardBuilder
from state.uload_log import Upload_logState
from state.upload_lotw import Upload_lotwState
from aiogram.types import FSInputFile
from aiogram.fsm.state import default_state
from state.register import PaperQSLState
from handlers.create_pdf import create_w100c_pdf, create_w100l_pdf, create_w1000b_pdf, create_w1000u_pdf, create_w25r_pdf
import sqlite3
import os
import re

# Инициализируем роутер уровня модуля
router = Router()

@router.callback_query(F.data == 'menu_utilites')
async def menu_utilites(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.convert.log(), callback_data='conv_log')
    kb.button(text='🧑‍🚀 Выписка по диплому Cosmos', callback_data='app_cosmos')
    kb.button(text='Потвердить страну, регион РФ бумажной QSL', callback_data='paper_qsl')
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(1)
    await bot.send_message(callback.from_user.id, 'Утилиты', reply_markup=kb.as_markup())

@router.callback_query(F.data == 'app_cosmos')
async def app_cosmos(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
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
    document = FSInputFile(file_path)
    await bot.send_document(callback.from_user.id, document)
    await bot.send_message(callback.from_user.id, text=
                        f'📌 <b>{user}</b> в завке на диплом Cosmos <b>{len(cosmos_log)}</b> уникальных позывных.\n\n'
                        f'💾 Файл выписки заявки на диплом Cosmos 👇 \n\n'
                        , reply_markup=kb.as_markup())

@router.callback_query(F.data == 'paper_qsl')
async def paper_qsl(callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, 'Отправьте фото QSL')
    await state.set_state(PaperQSLState.msg)

@router.message(StateFilter(PaperQSLState.msg))
async def paper_qsl_msg(message: types.Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = 'From ' + db.select_user_id(message.from_user.id)[1]


    if message.text is not None:
        await bot.send_message(537513849, user + '\n'+ message.text)

    elif message.photo is not None:
        await bot.send_photo(537513849, photo=message.photo[-1].file_id,
                             caption=user)

    elif message.document is not None:
        await bot.send_document(537513849, document=message.document.file_id,
                                caption=user)
    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text='Отправить другую сторону или еще что-то', callback_data='paper_qsl')
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(1)
    await bot.send_message(message.from_user.id, f'Отправлено', reply_markup=kb.as_markup())



