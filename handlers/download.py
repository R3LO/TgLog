# -*- coding: UTF-8 -*-
from aiogram import Bot
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
from aiogram.types import FSInputFile
from aiogram.fsm.state import default_state
from handlers.create_pdf import create_w100c_pdf, create_w100l_pdf, create_w1000b_pdf, create_w1000u_pdf, create_w25r_pdf
import sqlite3
import os

# Инициализируем роутер уровня модуля
router = Router()

@router.callback_query(F.data == 'download')
async def main_menu_download(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.download.csv(), callback_data='dwnl_log_csv'),
    kb.button(text=i18n.download.adif(), callback_data='dwnl_log_adif')
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(2)
    await bot.send_message(callback.from_user.id, i18n.download.title(), reply_markup=kb.as_markup())

@router.callback_query(F.data == 'dwnl_log_csv')
async def dwnl_log_csv(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    qsos = db.get_full_log(user)
    if len(qsos) != 0:
        file = 'logs/' + user + '_' +'.csv'
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(file_path, 'w') as f:
            for i in range(len(qsos)):
                L = ''
                # L = f'{qsos[i][0]};{qsos[i][1]};{qsos[i][2]};{qsos[i][3]};{qsos[i][4]};{qsos[i][5]}\n'
                L += str(qsos[i][0]) + ';'
                L += str(qsos[i][1])  + ';'
                L += str(qsos[i][2]) + ';'
                L += str(qsos[i][3]) + ';'
                L += str(qsos[i][4]) + ';'
                L += str(qsos[i][5]) + ';'
                L += str(qsos[i][7]) + ';'
                L += str(qsos[i][8]) + ';'
                L += str(qsos[i][6]) + ';'
                L += '\n'
                f.writelines(L)
        await bot.send_message(callback.from_user.id, text=i18n.download.file(user=user, qsos=len(qsos)))
        document = FSInputFile(file_path)
        await bot.send_document(callback.from_user.id, document)
    else:
        await bot.send_message(callback.from_user.id, text=i18n.download.nothing())


@router.callback_query(F.data == 'dwnl_log_adif')
async def dwnl_log_adif(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    qsos = db.get_full_log(user)
    if len(qsos) != 0:
        file = 'logs/' + user + '_' +'.adif'
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(file_path, 'w') as f:
            L = f'TLog ADIF export file for {user}\n<EOH>\n'
            f.writelines(L)
            for i in range(len(qsos)):
                L = ''
                L += f'<CALL:{len(qsos[i][4].strip())}>{qsos[i][4].strip()} '
                qso_date = qsos[i][0].replace('-', '')
                L += f'<QSO_DATE:{len(qso_date)}>{qso_date} '
                time_on = qsos[i][1].replace(':', '')
                L += f'<TIME_ON:{len(time_on)}>{time_on} '
                L += f'<BAND:{len(qsos[i][2].strip())}>{qsos[i][2].strip()} '
                L += f'<MODE:{len(qsos[i][3].strip())}>{qsos[i][3].strip()} '
                if qsos[i][5] is not None:
                    L += f'<GRIDSQUARE:{len(qsos[i][5].strip())}>{qsos[i][5].strip()} '
                L += f'<OPERATOR:{len(qsos[i][6].strip())}>{qsos[i][6].strip()} '
                L += f'<PROP_MODE:3>SAT <SAT_NAME:6>QO-100 <EOR>\n'
                f.writelines(L)
        await bot.send_message(callback.from_user.id, text=i18n.download.file(user=user, qsos=len(qsos)))
        document = FSInputFile(file_path)
        await bot.send_document(callback.from_user.id, document)
    else:
        await bot.send_message(callback.from_user.id, text=i18n.download.nothing())