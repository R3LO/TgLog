from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
from utils.database import Database
# from keyboards.menu_kb import main_menu
from keyboards.main_kb import main_kb
import re
import os
import asyncio


async def start_register(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await bot.send_message(message.from_user.id, f'Вы уже зарегистрированы на позывной <b>{users[1]}</b>')
    else:
        await bot.send_message(message.from_user.id, f'⭐️ <b>Давайте начнем регистрацию</b> ⭐️ \n\n'
                            f'➡️ Введите в сообщении 👇 ваш основной позывной. \n\n'
                            f'💡 На ваш позывной будет открыт специальный аппаратный журанл. Позывной должен быть без дробей. ')
        await state.set_state(RegisterState.regCall)

async def register_call(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'👌 Вы ввели позывной <b>{message.md_text.upper()}</b> ⭐️ \n\n'
                         f'➡️ Теперь введите в сообщении 👇 ваше имя и фаимилию. \n\n'
                         f'💡 Имя и фамилия будет использоваться для вставки в выдаваемые электронные дипломы от нашего сервиса. Можно указать только имя или что-то на ваше усмотрение.')
    await state.update_data(regcall=message.text.upper())
    await state.set_state(RegisterState.regName)

async def register_name(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(regname=message.text)

    reg_data = await state.get_data()
    reg_call = reg_data.get('regcall')
    reg_name = reg_data.get('regname')
    msg = f'👌 Вы ввели: \n ✅ Позывной: <b>{reg_call}</b> \n ✅ Ваше имя: <b>{reg_name}</b>'
    await bot.send_message(message.from_user.id, msg)
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_user(reg_call, reg_name, message.from_user.id)
    db.add_table_user(reg_call)
    await bot.send_message(message.from_user.id, '<b>Регистрация завершена успешно!</b> 👍 \n\n<i>Для продолжения работы выберите действие из главного меню</i>', reply_markup=main_kb)
    # await asyncio.sleep(2)
    # await bot.send_message(message.from_user.id, '\n\n<b>☰ Главное меню</b>', reply_markup=main_menu())
    await state.clear()
