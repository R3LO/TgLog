from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


register_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text='✅ РЕГИСТРАЦИЯ'
            )
        ]
    
    ], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Нажмите на кнопку Регистрация'
    
)
