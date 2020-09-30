from aiogram.types import Message, CallbackQuery
from source.database import User


class Event:
    def __init__(self, id: int, call=None, message=None, user=None, **kwargs):
        self.name = 'Generic'
        self.message: Message = message
        self.call: CallbackQuery = call
        self.user: User = user
        self.id = id


    async def execute(self):
        pass

    @staticmethod
    async def before(message: Message, **kwargs):
        pass

    async def after(self):
        pass

    def __repr__(self):
        return f'<Event name={self.name} user={self.user}>'
