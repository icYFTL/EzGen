import requests
import json
import base64

data = json.dumps({
    'token': '7df8aa0a6ef41b9eef34116c0638f2ff',
    'group_name': 'ИКБО-12-19',
    'student_snp': 'Петров Петр Петрович',
    'teacher_snp': 'Иванов Иван Викторович',
    'year': 2020,
    'prac_number': 2,
    'code': base64.encodebytes(open('C:\\Users\\icyftl\\Desktop\\test.zip', 'rb').read()).decode('UTF-8')
}, ensure_ascii=False)


r = requests.post('https://icyftl.ru/ezgen/api/generate', data=data.encode('UTF-8'))
if r.status_code != 200:
    print(r.text)
    exit()

open('result.zip', 'wb').write(r.content)