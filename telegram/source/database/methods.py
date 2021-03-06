from core import Session
from source.database.user import User


def get_user(chat_id=None, id=None):
    if not chat_id and not id:
        return None

    if chat_id:
        _res = [x for x in Session().query(User).filter(User.chat_id == chat_id)]
        return _res[0] if _res else None

    if id:
        _res = [x for x in Session().query(User).filter(User.id == id)]
        return _res[0] if _res else None


def is_hash_unique(hash: str) -> bool:
    return not bool([x for x in Session().query(User).filter(User.hash == hash)])


def add_user(id: int, chat_id: int, status="inactive") -> User:
    _user = User(id=id, chat_id=chat_id, status=status)
    _sess = Session()
    _sess.add(_user)
    _sess.commit()

    return _user


def set_args(args: dict, user: User) -> None:
    _sess = Session()
    _sess.query(User).filter(User.id == user.id). \
        update(args, synchronize_session=False)
    _sess.commit()


def set_hash(hash: str, user: User) -> None:
    set_args({User.hash: hash}, user)


def set_status(status: str, user: User) -> None:
    set_args({User.status: status}, user)


def set_language(language: str, user: User) -> None:
    set_args({User.language: language}, user)


def set_group(group: str, user: User) -> None:
    set_args({User.group: group}, user)


def set_student(student: str, user: User) -> None:
    set_args({User.student_snp: student}, user)


def set_teacher(teacher: str, user: User) -> None:
    set_args({User.teacher_snp: teacher}, user)


def set_event(event: str, user: User) -> None:
    set_args({User.event: event}, user)