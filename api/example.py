import requests
import json
import base64

data = json.dumps({
    'token': 'dd1c0d67fbe55db9042cc7855314448307d300fa73180839b91545cb64957c400301385fc9b8d672263d5',
    'group_name': 'ИКБО-12-19',
    'student_snp': 'Петров Петр Петрович',
    'teacher_snp': 'Иванов Иван Викторович',
    'year': 2020,
    'prac_number': 1,
    'code': base64.encodebytes(open('/Users/icyftl/Desktop/test.zip', 'rb').read()).decode('UTF-8')
}, ensure_ascii=False)


r = requests.post('https://icyftl.ru/ezgen/api/generate', data=data.encode('UTF-8'))
if r.status_code != 200:
    print(r.text)
    exit()

open('result.zip', 'wb').write(r.content)