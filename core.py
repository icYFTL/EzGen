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

engine = create_engine(f'sqlite:///ezgen.db', echo=False)
Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)