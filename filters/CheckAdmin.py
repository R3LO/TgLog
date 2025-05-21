from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.database import Database
import os

class CheckAdmin(BaseFilter):
    async def __call__(self, message: Message):
        try:
            admin_id = os.getenv('ADMIN_ID')
            db = Database(os.getenv('DATABASE_NAME'))
            user = db.select_user_id(message.from_user.id)
            return (user[3] == admin_id)
        except:
            return False