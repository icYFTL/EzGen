from source.telegram_api._events import Event
from source.telegram_api.checks import token_check
from source.database.methods import set_status, set_token
from core import text
from source.telegram_api.keyboards import main_menu
from source.static.staticData import events_storage
from source.static.methods import del_event


class Activation(Event):
    def __init__(self, id: int, call=None, message=None, user=None, **kwargs):
        super().__init__(id, call, message, user, **kwargs)
        self.name = 'activation'

    async def execute(self) -> None:
        if not self.message or not self.user:
            raise ValueError('user or message instance empty')

        if token_check(self.message.text):
            set_status('active', self.user)
            set_token(self.message.text, self.user)
            self.__status = True, text[self.user.language]['welcome'].format(
                user=self.message.from_user.full_name), main_menu(self.user.language)
        else:
            self.__status = False, text[self.user.language]['invalid_token'], 0

    async def after(self) -> None:
        if self.__status[0]:
            del_event(self.id)
        if self.__status[2] == 0:
            await self.message.answer(text=self.__status[1])
        else:
            await self.message.answer(text=self.__status[1], reply_markup=self.__status[2])

    def __repr__(self):
        return f'<Event name={self.name} user={self.user}>'
