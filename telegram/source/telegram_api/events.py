from core import dp, config, bot
from aiogram.types import Message, CallbackQuery
from source.database.methods import *
from source.telegram_api.keyboards import *
import re
from source.static.staticData import events_storage
from source.ezgen_api.ezGenApi import EzGenAPI
from base64 import encodebytes
from source.telegram_api._events import *
from source.telegram_api.types.request import *
from source.static.methods import *


@dp.message_handler(commands=['start'])
async def on_start(message: Message):
    user: User = await get_user(message.chat.id)
    if not user:
        await add_user(id=message.from_user.id, chat_id=message.chat.id)
        await message.answer(text=config['start_msg'], reply_markup=lang_choice)
    elif user.status == 'inactive':
        await message.answer(text=config['start_msg'], reply_markup=lang_choice)
    else:
        await message.answer(text=text[user.language]['welcome'].format(user=message.from_user.full_name),
                             reply_markup=main_menu(
                                 user.language
                             ))


async def clear(instance, user: User) -> None:
    try:
        await instance.message.edit_text(text[user.language]['welcome'].format(user=instance.from_user.full_name))
        await instance.message.edit_reply_markup(main_menu(user.language))
    except:
        await instance.answer(text[user.language]['welcome'].format(user=instance.from_user.full_name),
                              reply_markup=main_menu(user.language))


@dp.message_handler(content_types=['document'])
async def code_handler(message: Message):
    user: User = await get_user(id=message.from_user.id)
    if [x for x in get_events(user_id=user.id) if x['event'] == 'request.code']:
        file = await bot.get_file(message.document.file_id)
        io_object = await bot.download_file(file.file_path)
        try:
            prac_num = get_report(message.from_user.id)['prac_num']
        except:
            await message.answer(text[user.language]['smth_went_wrong'])
            await clear(message, user)
            return
        ezapi_instance = EzGenAPI(
            prac_num=prac_num,
            code=encodebytes(io_object.read()).decode('UTF-8'),
            user=user
        )

        report = await ezapi_instance.generate_report()

        if not report[0]:
            await message.answer(report[1])
            await clear(message, user)
            return

        result = await bot.send_document(chat_id=user.chat_id,
                                         document=report[1],
                                         caption='Result:')

        if not result:
            await message.answer(text[user.language]['smth_went_wrong'])
            await clear(message, user)
            return
        await clear(message, user)


@dp.message_handler()
async def on_any(message: Message):
    user: User = await get_user(id=message.from_user.id)

    for record in events_storage:
        if record['user_id'] == user.id:
            if record.get('kwargs'):
                inst: Event = record['event'](user=user,
                                              message=message,
                                              id=record['id'],
                                              **record['kwargs'])
            else:
                inst: Event = record['event'](user=user,
                                              message=message,
                                              id=record['id'])
            await inst.execute()
            await inst.after()
            break


@dp.callback_query_handler(text_contains='cancel')
async def cancel_event(call: CallbackQuery):
    data = call.data

    position = data.split(':')[-1]
    user: User = await get_user(id=call.from_user.id)

    if position == 'menu':
        await call.message.edit_text(text[user.language]['welcome'].format(user=call.from_user.full_name))
        await call.message.edit_reply_markup(main_menu(user.language))


@dp.callback_query_handler(text_contains='menu')
async def menu_handler(call: CallbackQuery):
    data = call.data

    event = data.split(':')[-1]
    user: User = await get_user(id=call.from_user.id)

    if event == 'update_info':
        await call.message.edit_text(text[user.language]['sector_update'].format(
            info='''{group_text}
{student_text}
{teacher_text}'''.format(
                group_text=text[user.language]['group'].format(
                    group=user.group or 'None'
                ),
                student_text=text[user.language]['student_snp'].format(
                    snp=user.student_snp or 'None'
                ),
                teacher_text=text[user.language]['teacher_snp'].format(
                    snp=user.teacher_snp or 'None'
                )

            )
        ))
        await call.message.edit_reply_markup(sector_update_menu(user.language))
    elif event == 'new_prac':
        if not user.group or not user.student_snp or not user.teacher_snp:
            await call.message.edit_text(text[user.language]['basic_info_did_not_pass'])
            await call.message.edit_reply_markup(main_menu(user.language))
            return
        await call.message.edit_text(PracNum.request(user.language))
        new_event(event=Request, user_id=user.id, rtype=PracNum)
        try:
            await call.message.edit_reply_markup(None)
        except:
            pass


@dp.callback_query_handler(text_contains='sector')
async def update_sector(call: CallbackQuery):
    data = call.data

    sector = data.split(':')[-1]
    user: User = await get_user(id=call.from_user.id)

    if sector == 'all':
        new_event(
            event=Request,
            user_id=user.id,
            rtype=Group
        )
        new_event(
            event=Request,
            user_id=user.id,
            rtype=Student
        )
        new_event(
            event=Request,
            user_id=user.id,
            rtype=Teacher
        )
        await call.message.edit_text(text[user.language]['group_request'])
        try:
            await call.message.edit_reply_markup(None)
        except:
            pass
    elif sector == 'group':
        new_event(
            event=Request,
            user_id=user.id,
            rtype=Group
        )
        await call.message.edit_text(text[user.language]['group_request'])
        try:
            await call.message.edit_reply_markup(None)
        except:
            pass
    elif sector == 'student':
        new_event(
            event=Request,
            user_id=user.id,
            rtype=Student
        )
        await call.message.edit_text(text[user.language]['student_snp_request'])
        try:
            await call.message.edit_reply_markup(None)
        except:
            pass
    elif sector == 'teacher':
        new_event(
            event=Request,
            user_id=user.id,
            rtype=Teacher
        )
        await call.message.edit_text(text[user.language]['teacher_snp_request'])
        try:
            await call.message.edit_reply_markup(None)
        except:
            pass


@dp.callback_query_handler(text_contains='lang')
async def selecting_language(call: CallbackQuery):
    data = call.data

    lang = data.split(':')[-1].lower()
    user: User = await get_user(id=call.from_user.id)

    user.language = lang
    set_language(lang, user)

    answer = text['en']['selected_language'].format(lang='EN') \
        if lang == 'en' else text['ru']['selected_language'].format(lang='RU')

    await call.answer(text=answer)

    if user.status == 'inactive':
        new_event(event=Activation, user_id=user.id)
        await call.message.edit_text(text=text[lang]['activate_text'], parse_mode='MarkdownV2')
        try:
            await call.message.edit_reply_markup(reply_markup=None)
        except:
            pass
    else:
        await clear(call, user)
