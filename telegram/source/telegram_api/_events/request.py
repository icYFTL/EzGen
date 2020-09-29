from source.telegram_api._events import Event
from source.telegram_api.checks import token_check
from source.database.methods import set_group, set_teacher, set_student
from core import text
from source.telegram_api.keyboards import menu
from source.telegram_api.types.request import *
from source.telegram_api.checks.checks import *
from source.static.staticData import storage


class Request(Event):
    def __init__(self, **kwargs):
        self.name = 'Request'
        self.rtype = kwargs.get('rtype')
        super().__init__(**kwargs)

    def execute(self) -> tuple:
        if not isinstance(self.rtype, RType):
            raise ValueError('rtype is not <RType> object')
        if not self.instance or not self.user:
            raise ValueError('user or instance object empty')

        if self.rtype == Group:
            return self.__group()
        elif self.rtype == Student:
            return self.__student()
        elif self.rtype == Teacher:
            return self.__teacher()
        elif self.rtype == All:
            return self.__all()
        elif self.rtype == PracNum:
            return self.__prac_num()

    def __all(self) -> tuple:
        storage.append(
            {
                'user': self.user,
                'action': self.instance.answer,
                'args': Group.request(self.user.language),
                'event': Request(user=self.user,
                                 rtype=Group,
                                 instance=self.instance)
            },
            {
                'user': self.user,
                'action': self.instance.answer,
                'args': Student.request(self.user.language),
                'event': Request(user=self.user,
                                 rtype=Student,
                                 instance=self.instance)
            },
            {
                'user': self.user,
                'action': self.instance.answer,
                'args': Teacher.request(self.user.language),
                'event': Request(user=self.user,
                                 rtype=Teacher,
                                 instance=self.instance)
            }
        )
        return None, 0

    def __group(self):
        if not group_check(self.instance.text):
            return text[self.user.language]['invalid_info'].format(info='group'), 0
        set_group(self.instance.text, self.user)
        return text[self.user.language]['update_info_success'], 0

    def __student(self):
        if not group_check(self.instance.text):
            return text[self.user.language]['invalid_info'].format(info='student_snp'), 0
        set_student(self.instance.text, self.user)
        return text[self.user.language]['update_info_success'], 0

    def __teacher(self):
        if not group_check(self.instance.text):
            return text[self.user.language]['invalid_info'].format(info='teacher_snp'), 0
        set_teacher(self.instance.text, self.user)
        return text[self.user.language]['update_info_success'], 0

    def __prac_num(self) -> tuple:
        if not prac_check(self.instance.text):
            return text[self.user.language]['invalid_info'].format(info='prac_num'), 0

        storage.append({
            'user': self.user,
            'prac_num': self.instance.text
        })
        return None, 0

    def __repr__(self):
        return f'<Event name={self.name} user={self.user} type={self.rtype}>'
