from os import path, mkdir

if not path.exists('logs'):
    mkdir('logs')

from aiogram import executor
from source.telegram_api import dp

executor.start_polling(dp)
