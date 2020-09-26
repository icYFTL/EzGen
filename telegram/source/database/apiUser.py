from sqlalchemy import Column, Integer, String
from source.database import Base


class ApiUser(Base):
    __tablename__ = 'api_users'

    vk_user_id = Column(Integer, primary_key=True)
    token = Column(String)

    def __init__(self, vk_user_id: int, token: str):
        self.token = token
        self.vk_user_id = vk_user_id

    def __repr__(self):
        return f"<ApiUser(vk_id={self.vk_user_id})>"
