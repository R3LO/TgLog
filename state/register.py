from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    regCall = State()
    regName = State()