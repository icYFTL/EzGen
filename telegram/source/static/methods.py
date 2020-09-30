from source.static.staticData import events_storage, reports_storage
from source.telegram_api._events.event import Event


def get_last_event_id() -> int:
    return max([x['id'] for x in events_storage]) if events_storage else 0


def new_event(event: type(Event), user_id: int, **kwargs) -> None:
    events_storage.append({
        'id': get_last_event_id(),
        'event': event,
        'user_id': user_id,
        'kwargs': kwargs
    })


def del_event(id: int) -> bool:
    try:
        events_storage.remove([x for x in events_storage if x['id'] == id][0])
        return True
    except:
        return False


def get_events(id=None, user_id=None) -> list:
    if id:
        return [x for x in events_storage if x['id'] == id]
    elif user_id:
        return [x for x in events_storage if x['user_id'] == user_id]
    else:
        return []


def add_prac_number_report(user_id: int, prac_num: int) -> None:
    reports_storage.append({
        'user_id': user_id,
        'prac_num': prac_num
    })


def get_report(user_id: int) -> dict:
    return [x for x in reports_storage if x['user_id'] == user_id][0]
