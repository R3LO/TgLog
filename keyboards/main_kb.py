from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='☰ Меню'
        ),
        KeyboardButton(
            text='💼 Мой профиль'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False)