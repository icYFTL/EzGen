from source.telegram_api.events import Event
from source.telegram_api.checks import token_check
from source.database.methods import set_status
from core import text
from source.telegram_api.keyboards import menu


class Activation(Event):
    def __init__(self, **kwargs):
        self.name = 'Activation'
        super().__init__(**kwargs)

    def execute(self) -> tuple:
        if not self.instance or not self.user:
            raise ValueError('user or instance object empty')

        reply = None
        if token_check(self.instance.text):
            set_status('active', self.user)
            reply = text[self.user.language]['welcome'].format(self.instance.from_user.full_name), menu(self.user.language)
        else:
            reply = text[self.user.language]['invalid_token'], 0

        return reply

    def __repr__(self):
        return f'<Event name={self.name} user={self.user}>'
