from sqlalchemy import Column, Integer, String
from source.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    ip = Column(String, nullable=False, unique=True)
    hash = Column(String, nullable=False, unique=True)
    salt = Column(String, nullable=False)

    def __init__(self, ip: str, hash: str, salt: str):
        self.ip = ip
        self.hash = hash
        self.salt = salt

    def __repr__(self):
        return f"<User(id={self.id}, ip={self.ip})>"
