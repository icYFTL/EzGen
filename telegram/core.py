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
db_config = json.load(open('db_config.json', 'r', encoding='UTF-8'))
text = config['msg']


connect_str = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
engine = create_engine(connect_str.format(
    user=db_config['db_user'],
    password=db_config['db_password'],
    host=db_config['db_host'],
    name=db_config['db_name'],
    port=db_config['db_port']
), echo=False)
Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)

bot = Bot(token=config['tg_token'])
dp = Dispatcher(bot)