from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def interlinemenu():
    kb = InlineKeyboardBuilder()
    kb.button(text='📥 Загрузить лог', callback_data='upload_log'), kb.button(text='🔖 Синхронизация с LoTW', callback_data='upload_lotw')
    kb.button(text='💾 Скачать лог', callback_data='download_log'), kb.button(text='🗑 Удалить лог', callback_data='drop_log')
    kb.button(text='❌🛠 Конвертировать любой ADIF в QO-100 ADIF', callback_data='qo100_log')
    kb.button(text='❌🗞 Подробный поиск по логу', callback_data='full_search')
    kb.button(text='📊 Статистика', callback_data='statistics')
    kb.button(text='❌🏆 Мои дипломы', callback_data='my_diploma')
    kb.button(text='❌🆘 Помощь', callback_data='help')


    kb.adjust(2, 2, 1)
    return kb.as_markup()
