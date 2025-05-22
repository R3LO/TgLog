
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.types import CallbackQuery

async def CallBaksMenu(callback: CallbackQuery):
    if (callback.data == 'upload_log'):
        await callback.message.delete()
        await callback.message.answer('<b>Выбрано</b>: Загрузить лог')


    elif (callback.data == 'search_log'):
        await callback.message.delete()
        await callback.message.answer('Поиск по логу')
