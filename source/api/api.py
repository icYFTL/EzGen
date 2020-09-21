from flask import request, send_file
from core import app, theory
import json
from source.database.methods import *
from source.main.handler.builder import Builder
import io
import base64


@app.route('/ezgen/api/generate', methods=['GET'])
def on_generate_get():
    return '<h1>Use POST request instead GET</h1>', 405


@app.route('/ezgen/api', methods=['GET', 'POST'])
def root():
    return 'OK', 200


@app.route('/ezgen/api/generate', methods=['POST'])
def on_generate():
    if request.data:
        data = json.loads(request.data)
    else:
        return 'Empty JSON passed.', 400
    if not data.get('token'):
        return 'Empty token', 400

    _user = get_user(request.remote_addr)

    if not _user:
        return 'You are not registered in EzGen system.\nUse /ezgen/api/get_token', 400
    elif _user.hash != data['token']:
        return 'Invalid token.\nUse /ezgen/api/get_token', 400

    important_keys = ['group_name', 'student_snp', 'teacher_snp', 'year', 'prac_number', 'code']
    optional_keys = ['target_content', 'teor_content', 'conclusion_content', 'literature_used_content']

    for key in important_keys:
        if key not in data:
            return f'Empty key: "{key}"', 400

    builder = Builder(data['token'])

    file = io.BytesIO(base64.decodebytes(data['code'].encode('UTF-8')))

    if not builder.is_zip_file(file):
        return 'File\'s extension is not .zip', 400

    builder.generate_titul(
        group_name=data['group_name'],
        student_snp=data['student_snp'],
        teacher_snp=data['teacher_snp'],
        year=data['year']
    )

    prac_number = int(data['prac_number']) - 1

    if prac_number + 1 > len(theory['practice']) and [x for x in data.keys() if x not in optional_keys]:
        return f'Can\'t handle prac with {prac_number} number.\nOptional args needed.', 418

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


@app.route('/ezgen/api/get_token', methods=['GET'])
def on_token_get():
    user = get_user(request.remote_addr)
    if not user:
        user = add_user(request.remote_addr)

    return user.hash, 200
