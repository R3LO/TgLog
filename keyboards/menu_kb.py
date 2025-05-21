from aiogram.utils.keyboard import InlineKeyboardBuilder
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text='⚑ Загрузить лог', callback_data='upload_log')
    # kb.button(text='Загрузить лог2', callback_data='upload_log2')
    kb.adjust(1)
    
    return kb.as_markup()