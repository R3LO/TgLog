from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
          command='start',
          description='Запустить бот и показть меню'
        ),
        BotCommand(
          command='menu',
          description='Главное меню'
        ),
        BotCommand(
          command='cosmos',
          description='Сформировать заявку на диплом Cosmos Russia'
        )
        # BotCommand(
        #   command='stat_loc',
        #   description='Показать подтвержденные локаторы из LoTW'
        # ),
        # BotCommand(
        #   command='stat_cqz',
        #   description='Показать подтвержденные CQ зоны'
        # ),
        # BotCommand(
        #   command='stat_ituz',
        #   description='Показать подтвержденные ITU зоны'
        # ),
        # BotCommand(
        #   command='uniq_log',
        #   description='Подучить выписку уникальных позывных по логу'
        # ),
        # BotCommand(
        #   command='uniq_lotw',
        #   description='Подучить выписку уникальных позывных по LoTW'
        # )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())