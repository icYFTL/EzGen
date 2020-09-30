from core import text
import re


class RType(object):
    @staticmethod
    def regex() -> re:
        return re.compile('')

    @staticmethod
    def request(lang: str) -> str:
        return ''


class Token(RType):
    @staticmethod
    def regex() -> re:
        return re.compile(r'^[a-z0-9]{85}$')

    @staticmethod
    def request(lang: str) -> str:
        return text[lang]['activate_text']


class Group(RType):
    @staticmethod
    def regex() -> re:
        return re.compile(r'^[А-Яа-я0-9 \-.]+$')

    @staticmethod
    def request(lang: str) -> str:
        return text[lang]['group_request']


class SNP(RType):
    @staticmethod
    def regex() -> re:
        return re.compile(r'^([А-Яа-я\- .]+)$')

    @staticmethod
    def request(lang: str) -> str:
        return ''


class Student(SNP):
    @staticmethod
    def regex() -> re:
        super().__init__()

    @staticmethod
    def request(lang: str) -> str:
        return text[lang]['student_snp_request']


class Teacher(SNP):
    @staticmethod
    def regex() -> re:
        super().__init__()

    @staticmethod
    def request(lang: str) -> str:
        return text[lang]['teacher_snp_request']


class PracNum(RType):
    @staticmethod
    def regex() -> re:
        return '^[0-9]+$'

    @staticmethod
    def request(lang: str) -> str:
        return text[lang]['prac_num_request']


class Code(RType):
    @staticmethod
    def regex() -> re:
        return None

    @staticmethod
    def request(lang: str) -> str:
        return text[lang]['code_request']


class All(object):
    def __iter__(self):
        yield Group
        yield Student
        yield Teacher
