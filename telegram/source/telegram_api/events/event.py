from aiogram.types import Message
from source.database import User

class Event:
    def __init__(self, **kwargs):
        self.name = 'Generic'
        self.instance: Message  = kwargs.get('instance')
        self.user: User = kwargs.get('user')

    def execute(self):
        pass

    def __repr__(self):
        return f'<Event name={self.name} user={self.user}>'
