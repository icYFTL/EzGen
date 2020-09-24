import http3
from source.database.user import User
from datetime import datetime
import json


class EzGenAPI:
    def __init__(self, prac_num: int, code: str, user: User):
        self.prac_num = prac_num
        self.code = code
        self.user = user

    async def generate_report(self) -> tuple:
        client = http3.AsyncClient()
        r = await client.post(url='https://icyftl.ru/ezgen/api/generate', data=json.dumps({
            'group_name': self.user.group,
            'student_snp': self.user.student_snp,
            'teacher_snp': self.user.teacher_snp,
            'year': datetime.now().year,
            'prac_number': self.prac_num,
            'code': self.code,
            'token': self.user.hash
        }, ensure_ascii=False))
        if r.status_code != 200:
            return False, r.text
        return True, r.content
