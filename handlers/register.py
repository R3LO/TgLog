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
from aiogram.fsm.state import default_state
# from keyboards.main_kb import main_kb
import os

# Инициализируем роутер уровня модуля
router = Router()

# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message, i18n: TranslatorRunner,):
    await message.answer(
        text=i18n.nil.cancel())

# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, i18n: TranslatorRunner, state: FSMContext):
    await message.answer(text=i18n.reg.cancel())
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@router.callback_query(F.data == 'new_user_registration')
async def new_user_registration(callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    # await callback.message.delete()
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(callback.from_user.id)
    if (users):
        await bot.send_message(callback.from_user.id, f'Вы уже зарегистрированы на позывной <b>{users[1]}</b>')
    else:
        await bot.send_message(callback.from_user.id, text=i18n.regist.call())
        await state.set_state(RegisterState.regCall)


@router.message(StateFilter(RegisterState.regCall))
async def register_call(message: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    await state.update_data(regcall=message.text.upper())
    reg_data = await state.get_data()
    reg_call = reg_data.get('regcall')
    await bot.send_message(message.from_user.id, i18n.regist.name(reg_call=reg_call))
    await state.set_state(RegisterState.regName)

@router.message(StateFilter(RegisterState.regName), F.text.isalpha())
async def register_name(message: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    await state.update_data(regname=message.text)

    reg_data = await state.get_data()
    reg_call = reg_data.get('regcall')
    reg_name = reg_data.get('regname')
    await bot.send_message(message.from_user.id, i18n.regist.complit(reg_call=reg_call, reg_name=reg_name), reply_markup=interlinemenu(i18n))
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_user(reg_call, reg_name, message.from_user.id)
    # db.add_table_user(reg_call)
    await state.clear()
