from source.telegram_api.types.request import *


def token_check(token: str) -> bool:
    return bool(re.match(Token.regex(), token))


def snp_check(snp: str) -> bool:
    return bool(re.match(SNP.regex(), snp))


def group_check(group: str) -> bool:
    return bool(re.match(Group.regex(), group))


def prac_check(prac_num: str) -> bool:
    return bool(re.match(PracNum.regex(), prac_num))
