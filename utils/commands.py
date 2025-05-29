from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
          command='start'  ,
          description='Запустить бот'
        ),
        BotCommand(
          command='menu'  ,
          description='Показать кнопку Меню и Профиль'
        ),
        BotCommand(
          command='stat_states'  ,
          description='Показать страны подтвержденные страны DXCC из LoTW'
        ),
        BotCommand(
          command='stat_loc'  ,
          description='Показать подтвержденные локаторы из LoTW'
        ),
        BotCommand(
          command='stat_cqz'  ,
          description='Показать подтвержденные CQ зоны'
        ),
        BotCommand(
          command='stat_ituz'  ,
          description='Показать подтвержденные ITU зоны'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())