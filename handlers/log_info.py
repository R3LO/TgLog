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

@router.callback_query(F.data == 'log_info')
async def main_menu_log_info(callback: CallbackQuery, i18n: TranslatorRunner, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)[1]
    try:
        total_qsos_log = db.get_total_qso_log(user)
    except:
        await bot.send_message(callback.from_user.id, f'⚠️ Логи либо не загружены, либо ошибка базы данных.')
    print(total_qsos_log)
#     total_qsos_lotw = db.get_total_qso_lotw(user)
#     total_by_band = db.get_stat_bands(user)
#     band_msg = '👀 <b>По диапазонам в основном логе:</b>\n'
#     for i  in range(len(total_by_band)):
#         band_msg += f'▫️ {total_by_band[i][0]} ▫️ {total_by_band[i][1]} ▫️ {total_by_band[i][2]} QSO\n'
#     qsos = total_qsos_log[0][0]
#     lotws = total_qsos_lotw[0][0]
#     dxcc =  db.get_stat_states(user)
#     qra =  db.get_stat_loc(user)
#     cqz =  db.get_stat_cqz(user)
#     ituz =  db.get_stat_ituz(user)
#     uniq_log = db.get_total_uniq_log(user)
#     uniq_lotw = db.get_total_uniq_lotw(user)
#     # await callback.message.delete()
#     await bot.send_message(callback.from_user.id,
#                         f'📊 Статистика по логу <b>{user}</b>\n\n'
#                         f'✅ Всего загружено в лог:  <b>{qsos}</b> QSO\n'
#                         f'✅ Загружено LoTW:  <b>{lotws}</b> CFM\n\n'
#                         f'✅ Уникальных позывных на 🛰 QO-100:\n'
#                         f'▫️ по логу:  <b>{len(uniq_log)}</b> \n'
#                         f'▫️ по LoTW:  <b>{len(uniq_lotw)}</b> \n\n'
#                         f'{band_msg}'
#                         f'\n\n🏆 <b>ПО ДИПЛОМАМ НА 🛰 QO-100</b>\n'
#                         f'▫️LoTW DXCC:  {len(dxcc)} \n'
#                         f'▫️LoTW QRA локаторов:  {len(qra)} \n'
#                         f'▫️LoTW CQ зон:  {len(cqz)} \n'
#                         f'▫️LoTW ITU зон:  {len(ituz)} \n'
#                         f'\n\n💡 <i>Для допонительной информации можно выполнить команды:</i>\n'
#                         f'/stat_states - список подтверденных DXCC стран из LoTW\n'
#                         f'/stat_loc - спиок подтверденных локаторов из LoTW\n'
#                         f'/stat_cqz - спиок подтверденных CQ зон из LoTW\n'
#                         f'/stat_ituz - список подтверденных ITU зон из LoTW\n'
#                         f'/stat_ru - CFM Российские регионы в LoTW\n'
#                         f'/uniq_log - список уникальных позывных по логу\n'
#                         f'/uniq_lotw - список уникальных позывных по LoTW\n'

#                         )
# except:
#     await bot.send_message(callback.from_user.id, f'⚠️ Логи либо не загружены, либо ошибка базы данных.')