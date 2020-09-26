from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from source.database import Base
from source.database.apiUser import ApiUser


class User(Base):
    __tablename__ = 'telgram_users'

    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, ForeignKey(ApiUser.vk_user_id))
    chat_id = Column(Integer, nullable=True)
    status = Column(String, default="inactive")
    language = Column(String, nullable=True)
    group = Column(String, nullable=True)
    student_snp = Column(String, nullable=True)
    teacher_snp = Column(String, nullable=True)
    event = Column(String, nullable=True)
    api_user = relationship('ApiUser', uselist=False, backref='telegram_users')

    def __init__(self, id: int, chat_id: int, status: str):
        self.id = id
        self.chat_id = chat_id
        self.status = status

    def __repr__(self):
        return f"<User(id={self.chat_id}, status={self.status})>"
