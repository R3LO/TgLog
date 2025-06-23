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
from aiogram.fsm.state import default_state
import sqlite3
import os

# Инициализируем роутер уровня модуля
router = Router()

@router.callback_query(F.data == 'ranking')
async def main_menu_ranking(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.ranking.rus(), callback_data='ranking_russia')
    kb.button(text=i18n.ranking.dxcc(), callback_data='ranking_dxcc')
    kb.button(text=i18n.ranking.qthloc(), callback_data='ranking_loc')
    kb.button(text=i18n.ranking.unique(), callback_data='ranking_unique')
    kb.button(text=i18n.back(), callback_data='back_main_menu')
    kb.adjust(2, 2, 1)
    await bot.send_message(callback.from_user.id, i18n.ranking.title(), reply_markup=kb.as_markup())

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'back_main_menu')
async def back_main_menu(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, i18n.main.menu(), reply_markup=interlinemenu(i18n))

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'ranking_russia')
async def ranking_russia(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    # kb.button(text=f'🇷🇺 Регионы России', callback_data='ranking_russia')
    # kb.button(text=f'🌐 DXCC', callback_data='ranking_dxcc')
    # kb.button(text=f'🗂 QTH loc', callback_data='ranking_loc')
    # kb.button(text=f'🔰 Unique', callback_data='ranking_unique')
    kb.button(text=i18n.back(), callback_data='ranking')
    kb.adjust(3)
    # db = Database(os.getenv('DATABASE_NAME'))
    conn = sqlite3.connect('tgbot_QO100.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'
                        and name like '%_lotw'
                        order by name;""")
    # Получение результатов запроса
    tables = cursor.fetchall()
    dict_ru = {}
    msg = ''
    for table in tables:
        query_ru = f'''
                select count(*) as ru from (
                        SELECT state from {table[0]}
                        WHERE country in ('EUROPEAN RUSSIA', 'ASIATIC RUSSIA', 'KALININGRAD')
                        GROUP BY state
                        HAVING state <> ''
                        ORDER BY state ASC
                        )
                '''
        rus = cursor.execute(query_ru)
        res_rus = rus.fetchall()
        if res_rus[0][0]:
            table_rus = table[0].replace('_lotw', '')
            dict_ru[table_rus] = res_rus[0][0]
        dict_ru_sorted = sorted(dict_ru.items(), key=lambda item: item[1], reverse=True)
    for i in range(len(dict_ru_sorted)):
        msg = msg + f'{i+1} <b>{dict_ru_sorted[i][0]}</b> {dict_ru_sorted[i][1]}\n'
    await bot.send_message(callback.from_user.id, text=i18n.ranking.title() + '\n' + i18n.ranking.rus() + ' ' + i18n.ranking.based() + '\n' + msg, reply_markup=kb.as_markup())
    conn.close()

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'ranking_dxcc')
async def ranking_dxcc(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    # kb.button(text=f'🇷🇺 Регионы России', callback_data='ranking_russia')
    # kb.button(text=f'🇷🇺 Rus', callback_data='ranking_russia')
    # kb.button(text=f'🗂 QTH loc', callback_data='ranking_loc')
    # kb.button(text=f'🔰 Unique', callback_data='ranking_unique')
    kb.button(text=i18n.back(), callback_data='ranking')
    kb.adjust(3)
    # db = Database(os.getenv('DATABASE_NAME'))
    conn = sqlite3.connect('tgbot_QO100.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'
                        and name like '%_lotw'
                        order by name;""")
    # Получение результатов запроса
    tables = cursor.fetchall()
    dict_states = {}
    msg = ''
    for table in tables:
        query_states = f'''
            SELECT count(*) FROM (
               SELECT country FROM {table[0]}
                GROUP BY country
                HAVING country IS NOT NULL
            )
            ;
            '''
        states = cursor.execute(query_states)
        res_states = states.fetchall()
        if res_states[0][0]:
            table_states = table[0].replace('_lotw', '')
            dict_states[table_states] = res_states[0][0]
        dict_states_sorted = sorted(dict_states.items(), key=lambda item: item[1], reverse=True)
    for i in range(len(dict_states_sorted)):
        msg = msg + f'{i+1} <b>{dict_states_sorted[i][0]}</b> {dict_states_sorted[i][1]}\n'
    await bot.send_message(callback.from_user.id, text=i18n.ranking.title() + '\n' + i18n.ranking.dxcc() + ' ' + i18n.ranking.based() + '\n' + msg, reply_markup=kb.as_markup())
    conn.close()

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'ranking_loc')
async def ranking_loc(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    # kb.button(text=f'🇷🇺 Регионы России', callback_data='ranking_russia')
    # kb.button(text=f'🇷🇺 Rus', callback_data='ranking_russia')
    # kb.button(text=f'🌐 DXCC', callback_data='ranking_dxcc')
    # kb.button(text=f'🔰 Unique', callback_data='ranking_unique')
    kb.button(text=i18n.back(), callback_data='ranking')
    kb.adjust(3)
    # db = Database(os.getenv('DATABASE_NAME'))
    conn = sqlite3.connect('tgbot_QO100.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'
                        and name like '%_lotw'
                        order by name;""")
    # Получение результатов запроса
    tables = cursor.fetchall()
    dict_loc = {}
    msg = ''
    for table in tables:
        query_loc = f'''
                select count(*) from (
                    SELECT  substr(gridsquare, 1, 4) as loc from {table[0]}
                    group by loc
                    HAVING loc IS NOT NULL
                );
            '''
        loc = cursor.execute(query_loc)
        res_loc = loc.fetchall()
        if res_loc[0][0]:
            table_loc = table[0].replace('_lotw', '')
            dict_loc[table_loc] = res_loc[0][0]
        dict_loc_sorted = sorted(dict_loc.items(), key=lambda item: item[1], reverse=True)
    for i in range(len(dict_loc_sorted)):
        msg = msg + f'{i+1} <b>{dict_loc_sorted[i][0]}</b> {dict_loc_sorted[i][1]}\n'
    await bot.send_message(callback.from_user.id, text= i18n.ranking.title() + '\n' + i18n.ranking.qthloc() + ' ' + i18n.ranking.based() + '\n' + msg, reply_markup=kb.as_markup())
    conn.close()

# -------------------------------------------------------------------------------------

@router.callback_query(F.data == 'ranking_unique')
async def ranking_unique(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    await callback.message.delete()
    kb = InlineKeyboardBuilder()
    # kb.button(text=f'🇷🇺 Регионы России', callback_data='ranking_russia')
    # kb.button(text=f'🇷🇺 Rus', callback_data='ranking_russia')
    # kb.button(text=f'🌐 DXCC', callback_data='ranking_dxcc')
    # kb.button(text=f'🗂 QTH loc', callback_data='ranking_loc')
    kb.button(text=i18n.back(), callback_data='ranking')
    kb.adjust(3)
    # db = Database(os.getenv('DATABASE_NAME'))
    conn = sqlite3.connect('tgbot_QO100.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'
                        and name like '%_lotw'
                        order by name;""")
    # Получение результатов запроса
    tables = cursor.fetchall()
    dict_unique = {}
    msg = ''
    for table in tables:
        query_unique = f'''
                select count(*) from (
                    SELECT  call from {table[0]}
                    group by call
                );
            '''
        unique = cursor.execute(query_unique)
        res_unique = unique.fetchall()
        if res_unique[0][0]:
            table_unique = table[0].replace('_lotw', '')
            dict_unique[table_unique] = res_unique[0][0]
        dict_unique_sorted = sorted(dict_unique.items(), key=lambda item: item[1], reverse=True)
    for i in range(len(dict_unique_sorted)):
        msg = msg + f'{i+1} <b>{dict_unique_sorted[i][0]}</b> {dict_unique_sorted[i][1]}\n'
    await bot.send_message(callback.from_user.id, text=i18n.ranking.title() + '\n' + i18n.ranking.unique() + ' ' + i18n.ranking.based() + '\n' + msg, reply_markup=kb.as_markup())
    conn.close()

# -------------------------------------------------------------------------------------