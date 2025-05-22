from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def mmenu():
    # Создаем объекты инлайн-кнопок
    url_button_1 = InlineKeyboardButton(
        text='Курс "Телеграм-боты на Python и AIOgram"',
        url='https://stepik.org/120924'
    )
    url_button_2 = InlineKeyboardButton(
        text='Документация Telegram Bot API',
        url='https://core.telegram.org/bots/api'
    )

    # Создаем объект инлайн-клавиатуры
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[url_button_1],
                        [url_button_2]]
    )
    print(789)
    return keyboard

def interlinemenu():
    kb = InlineKeyboardBuilder()
    kb.button(text='⚑ Загрузить лог', callback_data='upload_log')
    # kb.button(text='Загрузить лог2', callback_data='upload_log2')
    kb.adjust(1)
    return kb.as_markup()
