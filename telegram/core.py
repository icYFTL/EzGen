from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import json
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from source.database import Base


logging.basicConfig(filename='logs/telegram.log', level=logging.INFO,
                    format='%(asctime)-15s | [%(name)s] %(levelname)s => %(message)s')

config = json.load(open('config.json', 'r', encoding='UTF-8'))
text = config['msg']

engine = create_engine(f'sqlite:///{config["db_name"]}', echo=False)
Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)

bot = Bot(token=config['tg_token'])
dp = Dispatcher(bot)