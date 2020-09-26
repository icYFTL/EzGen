from flask import request, send_file
from core import app, theory, config
import json
from source.database.methods import *
from source.main.handler.builder import Builder
import io
import base64
import requests


@app.route('/ezgen/api/generate', methods=['GET'])
def on_generate_get():
    return '<h1>Use POST request instead GET</h1>', 405


@app.route('/ezgen/api', methods=['GET', 'POST'])
def root():
    return '<h1>OK</h1>', 200


def generate_reply(status: bool, content: str) -> json:
    return json.dumps({
        'status': status,
        'content': content
    })


@app.route('/ezgen/api/generate', methods=['POST'])
def on_generate():
    if request.data:
        data = json.loads(request.data)
    else:
        return generate_reply(False, 'Empty JSON passed'), 400
    if not data.get('token'):
        return generate_reply(False, 'Empty token'), 400

    _user = get_user(token=data['token'])

    if not _user:
        return generate_reply(False, 'You are not registered in EzGen system.\nUse /ezgen/api/authorize'), 400
    elif _user.token != data['token']:
        return generate_reply(False, 'Invalid token.\nUse /ezgen/api/authorize'), 400

    important_keys = ['group_name', 'student_snp', 'teacher_snp', 'year', 'prac_number', 'code']
    optional_keys = ['target_content', 'teor_content', 'conclusion_content', 'literature_used_content']

    for key in important_keys:
        if key not in data:
            return generate_reply(False, f'Empty key: "{key}"'), 400

    builder = Builder(data['token'])

    file = io.BytesIO(base64.decodebytes(data['code'].encode('UTF-8')))

    if len(file.read()) > 2097152:
        return generate_reply(False, 'Too large file.\nMax file size: 2 MB'), 406

    if not builder.is_zip_file(file):
        return generate_reply(False, 'File\'s extension is not .zip'), 400

    builder.generate_titul(
        group_name=data['group_name'],
        student_snp=data['student_snp'],
        teacher_snp=data['teacher_snp'],
        year=data['year']
    )

    prac_number = int(data['prac_number']) - 1

    if prac_number + 1 > len(theory['practice']) and [x for x in data.keys() if x not in optional_keys]:
        return generate_reply(False, f'Can\'t handle prac with {prac_number + 1} number.\nOptional args needed.'), 418

    builder.generate_prac_page(
        prac_number=prac_number + 1,
        target_content=theory['practice'][prac_number]['target'] if not data.get('target_content') else data.get(
            'target_content'),
        teor_content=theory['practice'][prac_number]['theory'] if not data.get('teor_content') else data.get('theory'),
        code_blocks=file,
        conclusion_content=theory['practice'][prac_number]['conclusion'] if not data.get(
            'conclusion_content') else data.get('conclusion_content'),
        literature_used_content=theory['practice'][prac_number]['literature'] if not data.get(
            'literature_used_content') else data.get('literature_used_content')

    )

    return send_file(builder.generate_result(), attachment_filename='result.zip')


@app.route('/ezgen/api/authorize', methods=['GET'])
def on_token_get():
    code = request.args.get('code')
    if code:
        access = json.loads(requests.get(
            f"https://oauth.vk.com/access_token?client_id=7609395&client_secret={config['app_secret']}&redirect_uri=https://icyftl.ru/ezgen/api/get_token&code=" + code).text)
        add_user(access['user_id'], access['token'])
        return generate_reply(True, access['token']), 200
    else:
        return generate_reply(False, 'Code arg is empty'), 400
