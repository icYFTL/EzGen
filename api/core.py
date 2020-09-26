import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from source.database import Base
from flask import Flask
import logging
from os import path, mkdir

if not path.exists('logs/'):
    mkdir('logs')

logging.basicConfig(filename='logs/ezgen.log', level=logging.INFO,
                    format=u'%(asctime)-15s | [%(name)s] %(levelname)s => %(message)s')

theory = json.load(open('source/static/theory.json', 'r', encoding='UTF-8'))
config = json.load(open('config.json', 'r'))

app = Flask(__name__)

connect_str = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
engine = create_engine(connect_str.format(
    user=config['db_user'],
    password=config['db_password'],
    host=config['db_host'],
    name=config['db_name'],
    port=config['db_port']
), echo=False)
Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)