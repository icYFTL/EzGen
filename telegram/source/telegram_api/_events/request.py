from source.telegram_api._events import Event
from source.telegram_api.checks import token_check
from source.database.methods import set_group, set_teacher, set_student
from core import text
from source.telegram_api.keyboards import main_menu, sector_update_menu
from source.telegram_api.types.request import *
from source.telegram_api.checks.checks import *
from source.static.staticData import events_storage
from source.static.methods import *
from aiogram.types import Message


class Request(Event):
    def __init__(self, id: int, call=None, message=None, user=None, **kwargs):
        super().__init__(id, call, message, user, **kwargs)
        self.name = 'request'
        self.rtype = kwargs.get('rtype')
        self.__status = None

    async def execute(self) -> None:
        # if self.rtype != type(RType):
        #     raise ValueError('rtype is not <RType> object')
        if not self.message or not self.user:
            raise ValueError('user or message instance empty')

        if self.rtype == Group:
            self.__group()
        elif self.rtype == Student:
            self.__student()
        elif self.rtype == Teacher:
            self.__teacher()
        elif self.rtype == PracNum:
            self.__prac_num()

    def __group(self) -> None:
        if not group_check(self.message.text):
            self.__status = False, text[self.user.language]['invalid_info'].format(info='group'), sector_update_menu(
                self.user.language)
            return
        set_group(self.message.text, self.user)
        self.__status = True, text[self.user.language]['update_info_success'], sector_update_menu(self.user.language)

    def __student(self) -> None:
        if not snp_check(self.message.text):
            self.__status = False, text[self.user.language]['invalid_info'].format(
                info='student_snp'), sector_update_menu(self.user.language)
            return
        set_student(self.message.text, self.user)
        self.__status = True, text[self.user.language]['update_info_success'], sector_update_menu(self.user.language)

    def __teacher(self) -> None:
        if not snp_check(self.message.text):
            self.__status = False, text[self.user.language]['invalid_info'].format(
                info='teacher_snp'), sector_update_menu(self.user.language)
            return
        set_teacher(self.message.text, self.user)
        self.__status = True, text[self.user.language]['update_info_success'], sector_update_menu(self.user.language)

    def __prac_num(self) -> None:
        if not prac_check(self.message.text):
            self.__status = True, text[self.user.language]['invalid_info'].format(info='prac_num'), sector_update_menu(
                self.user.language)
            return

        add_prac_number_report(self.user.id, int(self.message.text))
        new_event(
            event='request.code',
            user_id=self.user.id
        )
        self.__status = True, text[self.user.language]['code_request'], 0


    async def after(self):
        del_event(id=self.id)
        events = get_events(user_id=self.user.id)
        if not self.__status or (len(events) > 0 and get_events(user_id=self.user.id)[0]['event'] != 'request.code'):
            for event in events:
                rtype = event.get('kwargs', {}).get('rtype')
                if rtype:
                    await self.message.answer(
                        text=rtype.request(self.user.language)
                    )
                break
            return
        if self.__status[2] == 0:
            await self.message.answer(text=self.__status[1])
        else:
            await self.message.answer(text=self.__status[1], reply_markup=self.__status[2])



    def __repr__(self):
        return f'<Event name={self.name} user={self.user} type={self.rtype}>'
