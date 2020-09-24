from sqlalchemy import Column, Integer, String
from source.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=True)
    status = Column(String, default="inactive")
    language = Column(String, nullable=True)
    group = Column(String, nullable=True)
    student_snp = Column(String, nullable=True)
    teacher_snp = Column(String, nullable=True)
    event = Column(String, nullable=True)
    hash = Column(String, nullable=True)

    def __init__(self, id: int, chat_id: int, status: str):
        self.id = id
        self.chat_id = chat_id
        self.status = status

    def __repr__(self):
        return f"<User(id={self.chat_id}, status={self.status})>"
