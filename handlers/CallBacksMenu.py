# -*- coding: UTF-8 -*-

from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from state.uload_log import Upload_logState
from state.upload_lotw import Upload_lotwState
from state.conv_adif import Conv_AdifState
from keyboards.inline_menu_kb import interlinemenu
from utils.database import Database
from keyboards.inline_menu_kb import interlinemenu
from handlers.create_pdf import create_w100c_pdf, create_w100l_pdf, create_w1000b_pdf
import os
import re


# from aiogram.types import Message, FSInputFile


async def CallBaksMenu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(callback.from_user.id)

    if (user):
        if (callback.data == 'my_diploma'):
            '''
            Кнопка Мои дипломы

            '''
            await callback.message.delete()
            kb = InlineKeyboardBuilder()
            user = db.select_user_id(callback.from_user.id)[1]
            q_rus = len(db.get_stat_ru(user))
            q_rus_mark = '⭐️' if q_rus >= 25 else  '❌'
            q_loc = len(db.get_stat_loc(user))
            q_loc_mark = '⭐️' if q_loc >= 500 else  '❌'
            q_states = len(db.get_stat_states(user))
            q_states_mark = '⭐️' if q_states >= 100 else  '❌'
            q_unique = len(db.get_total_uniq_lotw(user))
            q_unique_mark = '⭐️' if q_unique >= 1000 else  '❌'
            q_base = db.get_total_qso_log(user)[0][0]
            q_base_mark = '⭐️' if q_unique >= 1000 else  '❌'
            kb.button(text=f'{q_rus_mark} W-QO100-R [{q_rus} из 25]', callback_data='dip_qo-100-russia')
            kb.button(text=f'{q_states_mark} W-QO100-C [{q_states} из 100]', callback_data='dip_qo-100-countries')
            kb.button(text=f'{q_loc_mark} W-QO100-L [{q_loc} из 500]', callback_data='dip_qo-100-locators')
            kb.button(text=f'{q_unique_mark} W-QO100-U [{q_unique} из 1000]', callback_data='dip_qo-100-unique')
            kb.button(text=f'{q_base_mark} W-QO100-B [{q_base} QSO]', callback_data='dip_qo-100-base')
            # kb.button(text='✓ Синхронизировать лог с LoTW', callback_data='upload_lotw')
            # kb.button(text='✗ Отмена', callback_data='clbk_cancel')
            kb.adjust(1)
            await bot.send_message(callback.from_user.id,
                                   f'🏆 <b>Дипломная программа 📡 QO-100-RUSSIA</b> \n\n'
                                   f'➡️ <b>W-QO100-R</b> - работал с 25 регионами 🇷🇺 России\n'
                                   f'➡️ <b>W-QO100-C</b> - работал со 100 странами по списку DXCC\n'
                                   f'➡️ <b>W-QO100-L</b> - работал с 500 различными QTH локаторами\n'
                                   f'➡️ <b>W-QO100-U</b> - работал с 1000 различными позывными\n'
                                   f'➡️ <b>W-QO100-B</b> - базовый диплом, 1000 связей в логе\n'
                                   f'\n<i>💡 Учитываются радиосвязи подтвержденные через LoTW</i>\n',
                                   reply_markup=kb.as_markup())


        if (callback.data == 'dip_qo-100-russia'):
            await bot.send_message(callback.from_user.id,
                                   f'⚠️ Выдача дипломов в стадии тестирования. QRX...')

# -----------------------------------------------------------------------------------------------------------------------------------------

        if (callback.data == 'dip_qo-100-locators'):
            await callback.message.delete()
            last_number = db.get_last_number_diplomas('w100l')[1]
            user = db.select_user_id(callback.from_user.id)[1]
            q_locators = len(db.get_stat_loc(user))
            if q_locators < 500:
                await bot.send_message(callback.from_user.id,
                                f'⚠️ Диплом <b>W-QO100-L</b> пока не выполнен.\n'
                                f'❗️Для получения диплома необходимо полученить QSL LoTW как минимум за работу с 500 QTH локаторами через 🛰 QO-100.\n'
                                f'💡 <i>Возможно вы не загрузили файл отчета из LoTW. \nПерейдите в Загрузку лога, нажмите на кнопку Синхронизировать лог с LoTW, отправьте файл отчета полученный с LoTW</i>\n')
            else:
                last_number += 1
                res =db.check_call_diplomas(user, 'w100l')
                kb = InlineKeyboardBuilder()
                kb.button(text=f'✅ Скачать PDF', callback_data='get_pdf_w100l')
                kb.button(text='✗ Отмена', callback_data='clbk_cancel')
                kb.adjust(1)

                if res: # есть в базе

                    await bot.send_message(callback.from_user.id,
                                    f'🏆 Вам выписан диплом <b>W-QO100-L</b> #{res[0]}.\n'
                                    '💡 <i>Диплом можно скачать в фломате PDF</i>', reply_markup=kb.as_markup())
                else: # нет в базе
                    db.add_call_diplomas(user, 'w100l', last_number)
                    await bot.send_message(callback.from_user.id,
                                    f'🏆 Поздравляем, диплом <b>W-QO100-L</b> #{last_number} выполнен.\n'
                                    '💡 <i>Диплом можно скачать в фломате PDF</i>', reply_markup=kb.as_markup())

        if (callback.data == 'get_pdf_w100l'):
            user = db.select_user_id(callback.from_user.id)
            res =db.check_call_diplomas(user[1], 'w100l')
            # print('user', user)
            # print('res', res)
            locators = len(db.get_stat_loc(user[1]))
            # print('locs', locators)
            create_w100l_pdf(user[1], user[2], res, locators)
            await bot.send_message(callback.from_user.id, text=
                            f'💾 PDF скоро будет готов. QRX... \n\n')
            pdf = user[1] + '_w500l.pdf'
            document = FSInputFile(pdf)
            await bot.send_document(callback.from_user.id, document)


# -----------------------------------------------------------------------------------------------------------------------------------------

        if (callback.data == 'dip_qo-100-countries'):
            await callback.message.delete()
            last_number = db.get_last_number_diplomas('w100c')[1]
            user = db.select_user_id(callback.from_user.id)[1]
            q_states = len(db.get_stat_states(user))
            if q_states < 100:
                await bot.send_message(callback.from_user.id,
                                f'⚠️ Диплом <b>W-QO100-C</b> пока не выполнен.\n'
                                f'❗️Для получения диплома необходимо полученить QSL LoTW как минимум за работу со 100 странами по списку DXCC через 🛰 QO-100.\n'
                                f'💡 <i>Возможно вы не загрузили файл отчета из LoTW. \nПерейдите в Загрузку лога, нажмите на кнопку Синхронизировать лог с LoTW, отправьте файл отчета полученный с LoTW</i>\n')
            else:
                last_number += 1
                res =db.check_call_diplomas(user, 'w100c')
                kb = InlineKeyboardBuilder()
                kb.button(text=f'✅ Скачать PDF', callback_data='get_pdf_w100c')
                kb.button(text='✗ Отмена', callback_data='clbk_cancel')
                kb.adjust(1)

                if res: # есть в базе

                    await bot.send_message(callback.from_user.id,
                                    f'🏆 Вам выписан диплом <b>W-QO100-C</b> #{res[0]}.\n'
                                    '💡 <i>Диплом можно скачать в фломате PDF</i>', reply_markup=kb.as_markup())
                else: # нет в базе
                    db.add_call_diplomas(user, 'w100c', last_number)
                    await bot.send_message(callback.from_user.id,
                                    f'🏆 Поздравляем, диплом <b>W-QO100-C</b> #{last_number} выполнен.\n'
                                    '💡 <i>Диплом можно скачать в фломате PDF</i>', reply_markup=kb.as_markup())

        if (callback.data == 'get_pdf_w100c'):
            user = db.select_user_id(callback.from_user.id)
            res =db.check_call_diplomas(user[1], 'w100c')
            states = len(db.get_stat_states(user[1]))
            # print(res)
            create_w100c_pdf(user[1], user[2], res[0], states)
            await bot.send_message(callback.from_user.id, text=
                            f'💾 PDF скоро будет готов. QRX... \n\n')
            pdf = user[1] + '_w100c.pdf'
            document = FSInputFile(pdf)
            await bot.send_document(callback.from_user.id, document)

# -----------------------------------------------------------------------------------------------------------------------------------------




        if (callback.data == 'dip_qo-100-unique'):
            await bot.send_message(callback.from_user.id,
                                   f'⚠️ Выдача дипломов в стадии тестирования. QRX...')

# -----------------------------------------------------------------------------------------------------------------------------------------

        if (callback.data == 'dip_qo-100-base'):
            await callback.message.delete()
            last_number = db.get_last_number_diplomas('w1000b')[1]
            user = db.select_user_id(callback.from_user.id)[1]
            q_qsos = db.get_total_qso_log(user)[0][0]
            if q_qsos < 1000:
                await bot.send_message(callback.from_user.id,
                                f'⚠️ Диплом <b>W-QO100-B</b> пока не выполнен.\n'
                                f'❗️Для получения диплома необходимо провести 1000 QSO через 🛰 QO-100.\n'
                                f'💡 <i>Возможно вы не загрузили QSO в основной лог. \nПерейдите в Загрузку лога, нажмите на кнопку Загрузить основной лог</i>\n')
            else:
                last_number += 1
                res =db.check_call_diplomas(user, 'w1000b')
                kb = InlineKeyboardBuilder()
                kb.button(text=f'✅ Скачать PDF', callback_data='get_pdf_w1000b')
                kb.button(text='✗ Отмена', callback_data='clbk_cancel')
                kb.adjust(1)

                if res: # есть в базе

                    await bot.send_message(callback.from_user.id,
                                    f'🏆 Вам выписан диплом <b>W-QO100-L</b> #{res[0]}.\n'
                                    '💡 <i>Диплом можно скачать в фломате PDF</i>', reply_markup=kb.as_markup())
                else: # нет в базе
                    print(res)
                    db.add_call_diplomas(user, 'w1000b', last_number)
                    await bot.send_message(callback.from_user.id,
                                    f'🏆 Поздравляем, диплом <b>W-QO100-L</b> #{last_number} выполнен.\n'
                                    '💡 <i>Диплом можно скачать в фломате PDF</i>', reply_markup=kb.as_markup())

        if (callback.data == 'get_pdf_w1000b'):
            user = db.select_user_id(callback.from_user.id)
            res =db.check_call_diplomas(user[1], 'w1000b')
            # print('user', user)
            # print('res', res)
            qsos = db.get_total_qso_log(user[1])[0][0]
            # print('qsos', qsos)
            create_w1000b_pdf(user[1], user[2], res[0], qsos)
            await bot.send_message(callback.from_user.id, text=
                            f'💾 PDF скоро будет готов. QRX... \n\n')
            pdf = user[1] + '_w1000b.pdf'
            document = FSInputFile(pdf)
            await bot.send_document(callback.from_user.id, document)


# -----------------------------------------------------------------------------------------------------------------------------------------


        if (callback.data == 'conv_log'):
            '''
            Кнопка конвертировать лог

            '''
            await callback.message.delete()
            await callback.message.answer(f'<b>Выбрано</b>: Конвертер QO-100')
            await callback.message.answer(
                                            f'⭐️ Загруженный файл при кнвертации не загружается в основную базу. Вы получите сконвертированный файл в ADIF формате. '
                                            f'После конвертации все теги BAND переписываются на <b>13CM</b>, добавляются дополнительные теги <b>PROP_MODE со значением SAT</b> и <b>SAT_NAME со значением QO-100</b>.\n\n'
                                            f'⭐️ <i>ADIF файл должен содердать минимум необходимых тегов:</i> \n\n'
                                            f'▫️QSO_DATE - дата QSO\n'
                                            f'▫️TIME_ON - время начало QSO\n'
                                            f'▫️CALL - позывной корреспондента\n'
                                            f'▫️MODE - вид связи\n'
                                            f'▫️SUBMODE - подвид связи, необязательное поле для цифровых видов \n'
                                            f'▫️GRIDSQUARE - локатор корреспондента (не обязательное поле)\n\n'
                                            f'💾 <b>Чтобы приступить к конфертации файла нажмите на 📎 или перетащите ADIF файл в это сообщенине.</b> \n\n'
                                            f'⚠️ <i>Для отмены загрузки отправьте текстовое сообшние <b>Отмена</b></i>')
            await state.clear()
            await state.set_state(Conv_AdifState.conv_adif)



        if (callback.data == 'main_menu_upload'):
            '''
            Кнопка загрузить

            '''
            await callback.message.delete()
            kb = InlineKeyboardBuilder()
            kb.button(text='✓ Загрузить основной лог', callback_data='upload_log'),
            kb.button(text='✓ Синхронизировать лог с LoTW', callback_data='upload_lotw')
            kb.button(text='✗ Отмена', callback_data='clbk_cancel')
            kb.adjust(1)
            await bot.send_message(callback.from_user.id,
                                   f'⭐️ Размер загружаемых файлов не более <b>10Мб</b> за раз. \n'
                                   f'⭐️ Формат загружаемых файлов <b>ADIF</b>. \n'
                                   f'⭐️ Повторные записи в лог не попадают. \n'
                                   f'⭐️ Загружаются связи только за <b>QO-100</b> диапаpон <b>13CM</b>. \n', reply_markup=kb.as_markup())


        if (callback.data == 'upload_lotw'):
            '''
            Кнопка Синхронизация с LoTW
            '''
            await callback.message.delete()
            await callback.message.answer(f'<b>Выбрано</b>: Снхронизация лога с файлом из LoTW')
            await bot.send_message(callback.from_user.id,
                                   f'⭐️ Для предотвращения \"утечек\" логина и пароля мы не запрашиваем данные сервиса LoTW, как это делают другие сервисы. Необходимый файл <b>lotwreport.adi</b> необходимо самостоятельно скачать из своей личной учетной записи LoTW. Скачанный <b>lotwreport.adi</b> файл должен быть не более <b>10Мб</b>. \n\n'
                                   f'1️⃣ Войдите в свою учетную запись LoTW \n'
                                   f'2️⃣ Перейдите в <b>Your QSOs</b> \n'
                                   f'3️⃣ Перейдите в <b>Download Report</b> \n'
                                   f'4️⃣ Поставьте галочки <b>Include QSL details</b> и вторая галочка на <b>Include QSO station details (\"my\" station location fields)</b> \n'
                                   f'5️⃣ Ниже выбирите позывной \n'
                                   f'6️⃣ Нажмите <b>Download Report</b> и сохрание файл себе на диск \n'
                                   f'7️⃣ Загрузите скачанный файл сообщением нажав на 📎 \n\n'
                                   f'<i>Для отмены загрузки отправьте текстовым сообшнием слово <b>Отмена</b></i>')
            await state.clear()
            await state.set_state(Upload_lotwState.upload_adif_lotw.state)


        if (callback.data == 'drop_log'):
            '''
            Кнопка Удалить логи

            '''
            kb = InlineKeyboardBuilder()
            kb.button(text='Удалить логи', callback_data='del_yes'),
            kb.button(text='Отмена', callback_data='clbk_cancel')
            kb.adjust(2)
            await callback.message.delete()
            await bot.send_message(callback.from_user.id,
                                   f'⚠️ <b>Вы дейсвтительно хотитте удалить логи?</b> \n\n'
                                   f'1️⃣ После удалнеия логов будет сброшена статистика. \n'
                                   f'2️⃣ Нельзя полчить дипломы \n'
                                   f'3️⃣ В любое время можно загрузить логи по новой. \n', reply_markup=kb.as_markup())
        if (callback.data == 'del_yes'):
            await callback.message.delete()
            db = Database(os.getenv('DATABASE_NAME'))
            user = db.select_user_id(callback.from_user.id)[1]
            db.delete_all_logs(user)
            await bot.send_message(callback.from_user.id,
                                   f'✅ <b>Ваши логи удалены!</b>\n\n'
                                   f'<i>Логи всегда можно загрузить снова в любой момент.\n</i>', reply_markup=interlinemenu())

        if (callback.data == 'clbk_cancel'):
            await callback.message.delete()
            await bot.send_message(callback.from_user.id,f'❌ <b>Действие отменено!</b>\n\n <b>☰ ГЛАВНОЕ МЕНЮ</b>', reply_markup=interlinemenu())

        if (callback.data == 'download_log'):
            '''
            Кнопка Скачать
            '''
            await callback.message.delete()
            kb = InlineKeyboardBuilder()
            kb.button(text='Формат CSV', callback_data='dwnl_log_csv'),
            kb.button(text='Формат ADIF', callback_data='dwnl_log_adif')
            kb.button(text='Отмена', callback_data='clbk_cancel')
            kb.adjust(2)
            await bot.send_message(callback.from_user.id,
                                   f'❓ <b>В каком формате вы хотите скачть лог?</b> \n\n'
                                   f'1️⃣ CSV можно открыть в Excel \n'
                                   f'2️⃣ ADIF можно загрузить в другие логи \n', reply_markup=kb.as_markup())
        if (callback.data == 'dwnl_log_csv'):
            '''
            Скачать лог в CSV формате

            '''
            await callback.message.delete()
            db = Database(os.getenv('DATABASE_NAME'))
            user = db.select_user_id(callback.from_user.id)[1]
            qsos = db.get_full_log(user)
            if len(qsos) != 0:
                file = 'logs/' + user + '_' +'.csv'
                file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
                with open(file_path, 'w') as f:
                    for i in range(len(qsos)):
                        L = ''
                        # L = f'{qsos[i][0]};{qsos[i][1]};{qsos[i][2]};{qsos[i][3]};{qsos[i][4]};{qsos[i][5]}\n'
                        L += str(qsos[i][0]) + ';'
                        L += str(qsos[i][1])  + ';'
                        L += str(qsos[i][2]) + ';'
                        L += str(qsos[i][3]) + ';'
                        L += str(qsos[i][4]) + ';'
                        L += str(qsos[i][5]) + ';'
                        L += str(qsos[i][6]) + ';'
                        L += '\n'
                        f.writelines(L)
                await bot.send_message(callback.from_user.id, text=
                            f'📌 <b>{user}</b> в логе <b>{len(qsos)}</b> QSO.\n\n'
                            f'💾 Файл лога в формате CSV ниже 👇 \n\n'
                            )
                document = FSInputFile(file_path)
                await bot.send_document(callback.from_user.id, document)
            else:
                await bot.send_message(callback.from_user.id, text='❌ Чтобы что-то скачать, нужно что-то загрузить!')


        if (callback.data == 'dwnl_log_adif'):
            '''
            Скачать лог в ADIF формате

            '''
            await callback.message.delete()
            db = Database(os.getenv('DATABASE_NAME'))
            user = db.select_user_id(callback.from_user.id)[1]
            qsos = db.get_full_log(user)
            if len(qsos) != 0:
                file = 'logs/' + user + '_' +'.adif'
                file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
                with open(file_path, 'w') as f:
                    L = f'TLog ADIF export file for {user}\n<EOH>\n'
                    f.writelines(L)
                    for i in range(len(qsos)):
                        L = ''
                        L += f'<CALL:{len(qsos[i][4].strip())}>{qsos[i][4].strip()}'
                        qso_date = qsos[i][0].replace('-', '')
                        L += f'<QSO_DATE:{len(qso_date)}>{qso_date}'
                        time_on = qsos[i][1].replace(':', '')
                        L += f'<TIME_ON:{len(time_on)}>{time_on}'
                        L += f'<BAND:{len(qsos[i][2].strip())}>{qsos[i][2].strip()}'
                        L += f'<MODE:{len(qsos[i][3].strip())}>{qsos[i][3].strip()}'
                        if qsos[i][5] is not None:
                            L += f'<GRIDSQUARE:{len(qsos[i][5].strip())}>{qsos[i][5].strip()}'
                        L += f'<OPERATOR:{len(qsos[i][6].strip())}>{qsos[i][6].strip()}'
                        L += f'<EOR>\n'
                        f.writelines(L)
                await bot.send_message(callback.from_user.id, text=
                            f'📌 <b>{user}</b> в логе <b>{len(qsos)}</b> QSO.\n\n'
                            f'💾 Файл лога в формате ADIF ниже 👇 \n\n'
                            )
                document = FSInputFile(file_path)
                await bot.send_document(callback.from_user.id, document)
            else:
                await bot.send_message(callback.from_user.id, text='❌ Чтобы что-то скачать, нужно что-то загрузить!')



        if (callback.data == 'full_search'):
            await bot.send_message(callback.from_user.id, f'⚠️ Полный поиск по логу в стадии тестирования')

        if (callback.data == 'qo100_log'):
            await bot.send_message(callback.from_user.id, f'⚠️ Конвертер в стадии тестирования')

        if (callback.data == 'statistics'):
            db = Database(os.getenv('DATABASE_NAME'))
            user = db.select_user_id(callback.from_user.id)[1]
            try:
                total_qsos_log = db.get_total_qso_log(user)
                total_qsos_lotw = db.get_total_qso_lotw(user)
                total_by_band = db.get_stat_bands(user)
                band_msg = '👀 <b>По диапазонам в основном логе:</b>\n'
                for i  in range(len(total_by_band)):
                    band_msg += f'▫️ {total_by_band[i][0]} ▫️ {total_by_band[i][1]} ▫️ {total_by_band[i][2]} QSO\n'
                qsos = total_qsos_log[0][0]
                lotws = total_qsos_lotw[0][0]
                dxcc =  db.get_stat_states(user)
                qra =  db.get_stat_loc(user)
                cqz =  db.get_stat_cqz(user)
                ituz =  db.get_stat_ituz(user)
                uniq_log = db.get_total_uniq_log(user)
                uniq_lotw = db.get_total_uniq_lotw(user)
                # await callback.message.delete()
                await bot.send_message(callback.from_user.id,
                                    f'📊 Статистика по логу <b>{user}</b>\n\n'
                                    f'✅ Всего загружено в лог:  <b>{qsos}</b> QSO\n'
                                    f'✅ Загружено LoTW:  <b>{lotws}</b> CFM\n\n'
                                    f'✅ Уникальных позывных на 🛰 QO-100:\n'
                                    f'▫️ по логу:  <b>{len(uniq_log)}</b> \n'
                                    f'▫️ по LoTW:  <b>{len(uniq_lotw)}</b> \n\n'
                                    f'{band_msg}'
                                    f'\n\n🏆 <b>ПО ДИПЛОМАМ НА 🛰 QO-100</b>\n'
                                    f'▫️LoTW DXCC:  {len(dxcc)} \n'
                                    f'▫️LoTW QRA локаторов:  {len(qra)} \n'
                                    f'▫️LoTW CQ зон:  {len(cqz)} \n'
                                    f'▫️LoTW ITU зон:  {len(ituz)} \n'
                                    f'\n\n💡 <i>Для допонительной информации можно выполнить команды:</i>\n'
                                    f'/stat_states - список подтверденных DXCC стран из LoTW\n'
                                    f'/stat_loc - спиок подтверденных локаторов из LoTW\n'
                                    f'/stat_cqz - спиок подтверденных CQ зон из LoTW\n'
                                    f'/stat_ituz - список подтверденных ITU зон из LoTW\n'
                                    f'/stat_ru - CFM Российские регионы в LoTW\n'
                                    f'/uniq_log - список уникальных позывных по логу\n'
                                    f'/uniq_lotw - список уникальных позывных по LoTW\n'

                                    )
            except:
                await bot.send_message(callback.from_user.id, f'⚠️ Логи либо не загружены, либо ошибка базы данных.')

        if (callback.data == 'help'):
            await bot.send_message(callback.from_user.id, f'⚠️ Помощь в стадии тестирования')


        if (callback.data == 'upload_log'):
            '''
            Загрузить основной лог ADIF

            '''
            await callback.message.delete()
            await callback.message.answer(f'<b>Выбрано</b>: Загрузить лог')
            await callback.message.answer(f'⭐️ <i><b>ADIF файла должен содердать теги:</b></i> \n\n'
                                            f'▫️QSO_DATE - дата QSO\n'
                                            f'▫️TIME_ON - время начало QSO\n'
                                            f'▫️CALL - позывной корреспондента\n'
                                            f'▫️MODE - вид связи\n'
                                            f'▫️SUBMODE - подвид связи, необязательное поле для цифровых видов \n'
                                            f'▫️<b>BAND - диапазон должен быть указан как 13CM</b>\n'
                                            f'▫️GRIDSQUARE - локатор корреспондента (не обязательное поле)\n\n'
                                            f'💾 <b>Чтобы приступить к загрузке нажмите на 📎 или перетащите файл лога в это сообщенине.</b> \n\n'
                                            f'⚠️ <i>Для отмены загрузки отправьте текстовое сообшние <b>Отмена</b></i>')
            await state.clear()
            await state.set_state(Upload_logState.upload_adif)



        # elif (callback.data == 'search_log'):
        #     await callback.message.delete()
        #     await callback.message.answer('Поиск по логу')
    else:
        await bot.send_message(callback.from_user.id, f'⚠️ Вам необходимо зарегистрироваться! Введите /start')

async def upload_adif_lotw(message: types.Message, state: FSMContext, bot: Bot):
    '''
    Обработка загруженого ADIF LoTW

    '''
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    if message.document:
        file = 'logs/' + user + '_' + str(message.from_user.id) +'_lotw.txt'
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        await message.bot.download(message.document, destination=file_path)
        file_size = os.path.getsize(file_path)
        if (file_size > 12 * 1024 * 1024):
            await bot.send_message(message.from_user.id, '⛔️ Размер файла более <b>12Мб</b>.\n\n')
            await state.clear()
            await bot.send_message(message.from_user.id, '<b>☰ ГЛАВНОЕ МЕНЮ</b>', reply_markup=interlinemenu())
            return
        await lotw(file_path, message, bot)
        await state.clear()
        await bot.send_message(message.from_user.id, '💡 <i>Вы можете начать пользоваться поиском по логу. Если сейчас в сообщением отправить мне часть позывного или локатора, то произойдет поиск по вашему логу по полю позывной или локатор.</i> \n\n Либо для продолжения выберите действие из меню.', reply_markup=interlinemenu())
    else:
        await message.reply("⛔️ Загрузка файла отменена.")
        await state.clear()
        await bot.send_message(message.from_user.id, 'Для продолжения выберите действие', reply_markup=interlinemenu())


async def upload_adif(message: types.Message, state: FSMContext, bot: Bot):
    '''
    Обработка загруженого ADIF основной лог

    '''
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    if message.document:
        file = 'logs/' + user + '_' + str(message.from_user.id) +'.txt'
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        await message.bot.download(message.document, destination=file_path)
        file_size = os.path.getsize(file_path)
        if (file_size > 10 * 1024 * 1024):
            await bot.send_message(message.from_user.id, '⛔️ Размер файла превышает 10Мб.\n\n')
            await state.clear()
            await bot.send_message(message.from_user.id, '☰ <b>ГЛАВНОЕ МЕНЮ</b>', reply_markup=interlinemenu())
            return
        # обраюботка ADIF
        await adif(file_path, message, bot)
        await state.clear()
        await bot.send_message(message.from_user.id, '💡 <i>Основной лог загружен. Для поиска по логу отправьте сообщением позывной или локатор.</i> \n\n ☰ <b>ГЛАВНОЕ МЕНЮ</b>', reply_markup=interlinemenu())
    else:
        await message.reply("⛔️ Загрузка основного лога отменена.")
        await state.clear()
        await bot.send_message(message.from_user.id, '☰ <b>ГЛАВНОЕ МЕНЮ</b>', reply_markup=interlinemenu())



async def lotw(file_path: str, message: Message, bot: Bot):
    '''
    Обработка LoTW ADIF файла
    '''
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    logbook = []
    raw = re.split('<EOR>|<EOH>', open(file_path, encoding="utf8", errors='ignore').read().upper(), flags=re.IGNORECASE)
    if (raw[0].split('\n')[0] == 'ARRL LOGBOOK OF THE WORLD STATUS REPORT'):
        try:
            for record in raw[1:-1]:
                if (':0><' in record): record = record.replace(':0><', ':1> <')
                qso = {}
                ADIF_REC_RE = re.compile(r'<(.*?):(\d+).*?>([^<\t\f\v]+)')
                tags = ADIF_REC_RE.findall(record)
                for tag in tags:
                    qso[tag[0].lower()] = tag[2][:int(tag[1])]
                    if (qso[tag[0].lower()] == 'MFSK'):
                        qso[tag[0].lower()] = 'FT4'
                if ('gridsquare' not in qso): qso['gridsquare'] = None
                if ('state' not in qso): qso['state'] = None
                if ('operator' not in qso): qso['operator'] = user
                logbook.append(qso)
        except:
            await bot.send_message(message.from_user.id, '❌ Не найдены ADIF теги.')
    else:
        await bot.send_message(message.from_user.id, '❌ Загруженный файл не с сайта ARRL LoTW')

    if (len(logbook) > 0):
        # n = len(logbook)
        await bot.send_message(message.from_user.id, f'✅ В файле LoTW <b>{len(logbook)}</b> QSL.')
        data = []
        try:
            n = 0
            for i in range(len(logbook)):
                if ('prop_mode' in logbook[i] and 'sat_name' in logbook[i]):
                    if (logbook[i]['band'] == '13CM' and logbook[i]['prop_mode'] == 'SAT' and logbook[i]['sat_name'] == 'QO-100'):
                        qso_date = logbook[i].get('qso_date')[:4] + '-' + logbook[i].get('qso_date')[4:6] + '-' + logbook[i].get('qso_date')[6:]
                        time_on = logbook[i].get('time_on')[:2] + ':' + logbook[i].get('time_on')[2:4] + ':' + logbook[i].get('time_on')[4:6]
                        data.append([logbook[i].get('call'), logbook[i].get('band'), logbook[i].get('mode'), qso_date, time_on, logbook[i].get('prop_mode'), logbook[i].get('sat_name'), logbook[i].get('qsl_rcvd'), logbook[i].get('dxcc'), logbook[i].get('country'), logbook[i].get('gridsquare'), logbook[i].get('state'), logbook[i].get('cqz'), logbook[i].get('ituz'), logbook[i].get('operator')])
                        n += 1
        except:
            pass
        db.add_table_user(user)
        db.add_user_lotw_data(user+'_lotw', data)


        await bot.send_message(message.from_user.id, f'✅ <b>{n}</b> QO-100 LoTW QSL загружены в базу.')





async def adif(file_log: str, message: Message, bot: Bot):
    '''
    Обработка ADIF основного лога

    '''
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    error = False
    file = 'logs/' + user + '_bad_log.txt'
    bad_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(bad_file_path, 'w'):   pass
    logbook = []
    try:
        raw = re.split('<EOR>|<EOH>', open(file_log, encoding="utf8", errors='ignore').read().upper(), flags=re.IGNORECASE)
    except:
        await bot.send_message(message.from_user.id, '❌ Это не файл ADIF лога')
        return
    try:
        for record in raw[1:-1]:
            if (':0><' in record): record = record.replace(':0><', ':1> <')
            qso = {}
            ADIF_REC_RE = re.compile(r'<(.*?):(\d+).*?>([^<\t\f\v]+)')
            tags = ADIF_REC_RE.findall(record)
            for tag in tags:
                qso[tag[0].lower()] = tag[2][:int(tag[1])]
                if (qso[tag[0].lower()] == 'MFSK'):
                    qso[tag[0].lower()] = 'FT4'
            if ('gridsquare' not in qso): qso['gridsquare'] = None
            if ('rst_rcvd' not in qso): qso['rst_rcvd'] = None
            if ('rst_sent' not in qso): qso['rst_sent'] = None
            logbook.append(qso)
    except:
        await bot.send_message(message.from_user.id, '❌ Не найдены ADIF теги.')

    if len(logbook) > 0:
        sum_qso = len(logbook)
        await bot.send_message(message.from_user.id, f'✅ Загружено <b>{sum_qso}</b> QSO. QRX...')
        data = []
        n = 0
        for i in range(len(logbook)):
            if (logbook[i].get('call') is not None) and (logbook[i].get('qso_date') is not None) and (logbook[i].get('time_on') is not None) and (logbook[i].get('band') is not None) and (logbook[i].get('mode') is not None):
                qso_date = logbook[i].get('qso_date')[:4] + '-' + logbook[i].get('qso_date')[4:6] + '-' + logbook[i].get('qso_date')[6:]
                time_on = logbook[i].get('time_on')[:2] + ':' + logbook[i].get('time_on')[2:4] + ':' + logbook[i].get('time_on')[4:6]
                logbook[i]['operator'] = user
                if (logbook[i].get('band') == '13CM'):
                    data.append([logbook[i].get('call'), qso_date, time_on, logbook[i].get('band'), logbook[i].get('mode'), logbook[i].get('gridsquare'), logbook[i].get('operator'), logbook[i].get('rst_rcvd'), logbook[i].get('rst_sent')])
                    n += 1
            else:
                error = True
                txt = '---=== Нет полных данных о QSO ===---\n' + '; '.join([f'{key.capitalize()}: {value}' for key, value in logbook[i].items()]) + '\n\n'
                with open(bad_file_path, 'a', encoding='utf-8') as f:
                    f.write(txt)
        db.add_table_user(user)
        db.add_user_qso_data(user, data)
        await bot.send_message(message.from_user.id, f'✅ <b>{n}</b> QSO за диапазон 13СМ добавлены в базу. \n')
        if error:
            await bot.send_message(message.from_user.id, f'❌ <b>При обработке файла возникли ошибки.</b> \n\n 💾 <i>Данные, которые не попали в базу, в прикрепленном файле ниже 👇</i>')
            document = FSInputFile(bad_file_path)
            await bot.send_document(message.from_user.id, document)
    else:
        await bot.send_message(message.from_user.id, '❌ В файле нет данных о QSO. Обработка завершена.')
        return


async def conv_adif(message: types.Message, state: FSMContext, bot: Bot):
    '''
    Обработка конвертиции ADIF файла

    '''
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    if message.document:
        pass
        file = 'logs/' + user + '_' + str(message.from_user.id) +'_conv.adi'
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        await message.bot.download(message.document, destination=file_path)
        file_size = os.path.getsize(file_path)
        if (file_size > 10 * 1024 * 1024):
            await bot.send_message(message.from_user.id, '⛔️ Размер файла превышает 10Мб.\n\n')
            await state.clear()
            await bot.send_message(message.from_user.id, '☰ <b>ГЛАВНОЕ МЕНЮ</b>', reply_markup=interlinemenu())
            return
        # обраюботка ADIF
        await conv_adif_process(file_path, message, bot)
        await state.clear()
        await bot.send_message(message.from_user.id, '☰ <b>ГЛАВНОЕ МЕНЮ</b>', reply_markup=interlinemenu())
    else:
        await message.reply("⛔️ Конвертация ADIF отменена.")
        await state.clear()
        await bot.send_message(message.from_user.id, '☰ <b>ГЛАВНОЕ МЕНЮ</b>', reply_markup=interlinemenu())

async def conv_adif_process(file_log: str, message: Message, bot: Bot):
    '''
    Обработка ADIF основного лога

    '''
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)[1]
    error = False
    file = 'logs/' + user + '_conv.adi'
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    logbook = []
    try:
        raw = re.split('<EOR>|<EOH>', open(file_log, encoding="utf8", errors='ignore').read().upper(), flags=re.IGNORECASE)
    except:
        await bot.send_message(message.from_user.id, '❌ Это не файл ADIF лога')
        return
    try:
        for record in raw[1:-1]:
            if (':0><' in record): record = record.replace(':0><', ':1> <')
            qso = {}
            ADIF_REC_RE = re.compile(r'<(.*?):(\d+).*?>([^<\t\f\v]+)')
            tags = ADIF_REC_RE.findall(record)
            for tag in tags:
                qso[tag[0].lower()] = tag[2][:int(tag[1])]
            # if ('gridsquare' not in qso): qso['gridsquare'] = ' '
            logbook.append(qso)
    except:
        await bot.send_message(message.from_user.id, '❌ Не найдены ADIF теги.')

    if len(logbook) > 0:
        sum_qso = len(logbook)
        await bot.send_message(message.from_user.id, f'✅ Загружено файл с <b>{sum_qso}</b> QSO.')
        data = []
        with open(file_path, 'w') as f:
            str = f'TLog converter for {user}\n<EOH>\n'
            f.writelines(str)
            for i in range(len(logbook)):
                logbook[i]['prop_mode'] = 'SAT'
                logbook[i]['sat_name'] = 'QO-100'
                logbook[i]['band'] = '13CM'
                # logbook[i]['operator'] = user
                str = ''
                for key in logbook[i]:
                    str += f'<{key.upper()}:{len(logbook[i][key])}>{logbook[i][key].upper()} '
                str += '<EOR>\n'
                f.writelines(str)
        await bot.send_message(message.from_user.id, f'💾 Файл ADIF преобразован 👇')
        document = FSInputFile(file_path)
        await bot.send_document(message.from_user.id, document)


    else:
        await bot.send_message(message.from_user.id, '❌ В файле нет данных о QSO. Обработка завершена.')
        return
