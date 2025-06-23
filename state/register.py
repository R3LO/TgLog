from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    regCall = State()
    regName = State()

class ProfileEditState(StatesGroup):
    editName = State()

class PaperQSLState(StatesGroup):
    msg = State()