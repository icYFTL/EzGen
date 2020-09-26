import re

def token_check(token: str) -> bool:
    return bool(re.match('^[a-z0-9]{32}$', token))

def snp_check(snp: str) -> bool:
    return bool(re.match('^([А-Яа-я\- .]+)\s([А-Я.]{2}){2}$', snp))
