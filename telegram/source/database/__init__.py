from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from source.database.user import User
from source.database.apiUser import ApiUser