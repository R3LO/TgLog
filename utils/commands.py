from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
          command='start',
          description='Start bot / Запустить бот'
        ),
        BotCommand(
          command='menu',
          description='Main menu / Главное меню'
        )

    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())