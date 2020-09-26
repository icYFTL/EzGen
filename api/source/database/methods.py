from core import Session
from source.database.user import User


def get_user(**args) -> User:
    if args.get('token'):
        _res = [x for x in Session().query(User).filter(User.token == args['token'])]
    elif args.get('vk_user_id'):
        _res = [x for x in Session().query(User).filter(User.vk_user_id == args['vk_user_id'])]
    else:
        raise ValueError
    return _res[0] if _res else None


def add_user(vk_user_id: int, token: str) -> User:
    _user = User(vk_user_id=vk_user_id, token=token)
    _sess = Session()
    _sess.add(_user)
    _sess.commit()

    return _user
