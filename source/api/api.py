from flask import request
from core import app, theory
import json
from source.database.methods import *
from source.main.handler.builder import Builder


@app.route('/ezgen/api/generate', methods=['GET'])
def on_generate_get():
    return 'Use post request instead', 405


@app.route('/ezgen/api', methods=['GET', 'POST'])
def root():
    return 'OK', 200


@app.route('/ezgen/api/generate', methods=['POST'])
def on_generate():
    data = json.loads(request.data)
    if not data.get('token'):
        return 'Empty token', 400

    if not get_user(request.remote_addr):
        return 'Invalid token', 400

    important_keys = ['group_name', 'student_snp', 'teacher_snp', 'year', 'prac_number', 'target_content',
                 'teor_content', 'conclusion_content', 'literature_used_content']

    for key in important_keys:
        if key not in data:
            return f'Empty key: "{key}"', 400

    if not request.files:
        return 'Zipped code didn\'t passed', 400

    file = request.files['code']

    if file.name.split('.'):
        if file.name.split('.')[-1] != 'zip':
            return 'File\'s extension is not .zip', 400
    else:
        return 'File\'s extension is not .zip', 400

    builder = Builder(data['token'])


    titul = builder.generate_titul(
        group_name=data['group_name'],
        student_snp=data['student_snp'],
        teacher_snp=data['teacher_snp'],
        year=data['year']
    )

    prac_number = int(data['prac_number'])

    prac_pages = builder.generate_prac_page(
        prac_number=prac_number,
        target_content=theory[prac_number]['target'] if not data.get('target_content') else data.get('target_content'),
        teor_content=theory[prac_number]['teor_content'] if not data.get('teor_content') else data.get('teor_content')

    )


@app.route('/ezgen/api/get_token', methods=['GET'])
def on_token_get():
    user = get_user(request.remote_addr)
    if not user:
        user = add_user(request.remote_addr)

    return user.hash, 200
