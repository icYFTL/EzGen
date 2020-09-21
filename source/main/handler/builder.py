from mako.template import Template
from html import escape
import zipfile
import io
from os import makedirs, path, walk
from shutil import rmtree
from datetime import datetime
import re
import logging
from source.static.methods import define_tmp_path


class Builder:
    def __init__(self, token: str):
        self.token = token
        self.pages = []
        self.logger = logging.getLogger('Builder')

    def generate_result(self):
        fp = zipfile.ZipFile(path.join(define_tmp_path(), self.token, str(int(datetime.now().timestamp()))), 'a')
        for page in self.pages:
            file = path.join(define_tmp_path(), self.token, page['filename'])
            open(file, 'wb').write(page['source'].encode('UTF-8'))
            fp.write(file)

        fp.close()
        return open(path.join(define_tmp_path(), self.token, str(int(datetime.now().timestamp()))), 'rb')

    def is_zip_file(self, file: io.BytesIO) -> bool:
        try:
            if not path.exists(path.join(define_tmp_path(), self.token, 'tmp')):
                makedirs(path.join(define_tmp_path(), self.token, 'tmp'))
            with zipfile.ZipFile(file) as _z:
                _z.extractall(path.join(define_tmp_path(), self.token, 'tmp'))
            rmtree(path.join(define_tmp_path(), self.token, 'tmp'))
            return True
        except Exception as e:
            self.logger.warning(e)
            return False

    def generate_titul(self, group_name: str,
                       student_snp: str,
                       teacher_snp: str,
                       year: int) -> None:
        self.pages.append({'source': Template(filename="source/static/templates/titul.html").render(group=group_name,
                                                                                                    student_snp=student_snp,
                                                                                                    teacher_snp=teacher_snp,
                                                                                                    year=year),
                           'filename': 'titul.html'})

    def generate_prac_page(self, prac_number: int,
                           target_content: str,
                           teor_content: str,
                           code_blocks: io.BytesIO,
                           conclusion_content: str,
                           literature_used_content: str) -> None:
        self.pages.append({'source': Template(filename='source/static/templates/practic.html').render(
            prac_number=prac_number,
            target_content=target_content,
            teor_content=teor_content,
            step_by_step=''.join(self.code_handler(code_blocks)),
            conclusion_content=conclusion_content,
            literature_used_content=literature_used_content
        ), 'filename': 'main.html'})

    def lf_beautify(self, content: str) -> str:
        return content.replace('\n', '<br>').replace('\\n', '<br>')

    def create_code_block(self, description: str, code: str):
        return f'''
<code>{self.lf_beautify(escape(code))}</code>
<strong>{self.lf_beautify(description)}</strong>
        '''

    def code_handler(self, zip_archive: io.BytesIO):
        box = str(int(datetime.now().timestamp()))

        root_path = path.join(define_tmp_path(), self.token)
        file_path = path.join(root_path, box + '.zip')

        if not path.exists(define_tmp_path()):
            makedirs(root_path)

        with zipfile.ZipFile(zip_archive, 'r') as _zip:
            _zip.extractall(file_path)

        for root, dirs, files in walk(file_path):
            for file in files:
                try:
                    if file.split('.'):
                        if file.split('.')[-1] != 'java':
                            raise IOError
                    else:
                        raise IOError
                except IOError:
                    return f'Not a .java file: {file}'

        code_blocks = []

        pic_num = 0

        for root, dirs, files in walk(file_path):
            for file in files:
                if file.split('.')[-1] == 'java' and not file.startswith('.'):
                    for block in self.__get_objects_from_java(open(path.join(root, file), 'r').read()):
                        code_blocks.append(self.create_code_block(description=f'Блок {pic_num}',
                                                                  code='\n\n' + block + '\n\n'
                                                                  ))
                        pic_num += 1

        return code_blocks

    def __get_objects_from_java(self, code: str) -> list:
        regex = r"(((|public|final|abstract|private|static|protected)(\s+))?(class)(\s+)(\w+)(<.*>)?(\s+extends\s+\w+)?(<.*>)?(\s+implements\s+)?(.*)?(<.*>)?(\s*))\{$(\s.*)+\}"

        matches = re.finditer(regex, code, re.MULTILINE)

        result = []

        for matchNum, match in enumerate(matches, start=1):
            result.append(match.group())

        return result
