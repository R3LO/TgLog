from aiogram import Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from state.uload_log import Upload_logState
from keyboards.inline_menu_kb import interlinemenu
import os


# from aiogram.types import Message, FSInputFile


async def CallBaksMenu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if (callback.data == 'upload_log'):
        await callback.message.delete()
        await callback.message.answer('<b>Выбрано</b>: Загрузить лог')
        await state.set_state(Upload_logState.upload_adif)


    elif (callback.data == 'search_log'):
        await callback.message.delete()
        await callback.message.answer('Поиск по логу')


async def upload_adif(message: types.Message, state: FSMContext, bot: Bot):

    if message.document:
        download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs.txt')
        await message.bot.download(message.document, destination=download_path)
        await state.clear()
        f = open(download_path, 'r')
        print('начинаю проверку...')
        log = f.read()
        # print(log)
        await bot.send_message(message.from_user.id, '<b>Лог получен</b> 👍 \n\n', reply_markup=interlinemenu())
        # print(file_path)
        # all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'All_logs')
        # adif_file = FSInputFile(path=os.path.join(all_media_dir, 'temp.txt'))
        # file = await message.bot.get_file(audio_file(adif_file)

        # await message.answer("Ваше аудиосообщение принято")
    else:
        await message.reply("⛔️ Отправьте файл лог в формате ADIF")
