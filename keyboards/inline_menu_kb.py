from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def interlinemenu():
    kb = InlineKeyboardBuilder()
    kb.button(text='⚑ Загрузить лог', callback_data='upload_log')
    kb.button(text='Поиск по логу', callback_data='search_log')
    kb.adjust(1)
    return kb.as_markup()
