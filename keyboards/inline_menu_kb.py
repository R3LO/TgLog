from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner



def interlinemenu(i18n: TranslatorRunner):
    kb = InlineKeyboardBuilder()
    # kb.button(text='📥 Загрузить лог', callback_data='upload_log'), kb.button(text='🔖 Синхронизация с LoTW', callback_data='upload_lotw')
    kb.button(text=i18n.upload.log(), callback_data='upload')
    kb.button(text=i18n.download.log(), callback_data='download')

    kb.button(text=i18n.users.raitings(), callback_data='ranking')
    kb.button(text=i18n.my.awards(), callback_data='awards')

    kb.button(text=i18n.worked.statistics(), callback_data='log_info')
    kb.button(text=i18n.profile(), callback_data='profile')

    kb.button(text='🛠 Утилиты', callback_data='menu_utilites')
    kb.button(text=i18n.wipe.log(), callback_data='wipe_log')

    kb.button(text='💡 Помощь', callback_data='menu_help')
    # kb.button(text=i18n.convert.log(), callback_data='conv_log')



    kb.button(text='🇷🇺 QO-100-RUSSIA', url='https://t.me/QO100RUSSIA/2')



    # kb.button(text='❌🆘 Помощь', callback_data='help')
    kb.adjust(2)
    return kb.as_markup()


def main_menu(i18n: TranslatorRunner):

    print(i18n.upload.log())

    return 0
