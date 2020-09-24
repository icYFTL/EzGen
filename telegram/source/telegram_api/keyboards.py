from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from source.telegram_api.callbackData import *
from core import text

lang_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='RU 🇷🇺', callback_data=lang_callback.new(selected='RU')),
            InlineKeyboardButton(text='EN 🇺🇸', callback_data=lang_callback.new(selected='EN'))
        ]
    ]
)


def activation(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text[lang]['activate_button'],
                                     callback_data=activation_callback.new(status='await')),
            ]
        ]
    )


def sector_update(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text[lang]['all_info'],
                                     callback_data=sector_callback.new(name='all'))
            ],
            [
                InlineKeyboardButton(text=text[lang]['group_button'],
                                     callback_data=sector_callback.new(name='group')),
                InlineKeyboardButton(text=text[lang]['student_snp_button'],
                                     callback_data=sector_callback.new(name='student')),
                InlineKeyboardButton(text=text[lang]['teacher_snp_button'],
                                     callback_data=sector_callback.new(name='teacher')),

            ],
            [
                InlineKeyboardButton(text=text[lang]['cancel'],
                                     callback_data=cancel_callback.new(position='menu'))
            ]
        ]
    )


def menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text[lang]['update_info_button'],
                                     callback_data=menu_callback.new(event='update_info')),
                InlineKeyboardButton(text=text[lang]['invoke_new_prac_button'],
                                     callback_data=menu_callback.new(event='new_prac')),
            ],
            [
                InlineKeyboardButton(text=text[lang]['change_lang_button'],
                                     callback_data=lang_callback.new(selected='ru' if lang == 'en' else 'en'))
            ]
        ]
    )
