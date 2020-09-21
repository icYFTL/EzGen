from core import Session
from source.database.user import User
from hashlib import md5
from random import randint


def get_user(ip: str) -> User:
    _res = [x for x in Session().query(User).filter(User.ip == ip)]
    return [x for x in Session().query(User).filter(User.ip == ip)][0] if _res else []


def add_user(ip: str) -> User:
    salt = ''.join([chr(randint(97, 122)) for _ in range(15)])
    hash = md5((ip + salt).encode('utf-8')).hexdigest()
    _user = User(ip=ip, hash=hash, salt=salt)
    _sess = Session()
    _sess.add(_user)
    _sess.commit()


    return _user
