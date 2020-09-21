from mako.template import Template
from html import escape
import zipfile
import io
from os import makedirs, path, walk
from datetime import datetime
import re


class Builder:
    def __init__(self, token: str):
        self.token = token

    def generate(self, pages: list):
        pass

    def generate_titul(self, group_name: str,
                       student_snp: str,
                       teacher_snp: str,
                       year: int) -> str:
        return Template(filename="source/static/templates/titul.html").render(group=group_name,
                                                                              student_snp=student_snp,
                                                                              teacher_snp=teacher_snp,
                                                                              year=year)

    def generate_prac_page(self, prac_number: int,
                           target_content: str,
                           teor_content: str,
                           code_blocks: bytes,
                           conclusion_content: str,
                           literature_used_content: str) -> str:
        return Template(filename='source/static/templates/practic.html').render(
            prac_number=prac_number,
            target_content=target_content,
            teor_content=teor_content,
            step_by_step=self.code_handler(code_blocks),
            conclusion_content=conclusion_content,
            literature_used_content=literature_used_content
        )

    def lf_beautify(self, content: str) -> str:
        return content.replace('\n', '<br>')

    def create_code_block(self, description: str, code: str):
        return f'''
<p>{Builder.lf_beautify(self, description)}</p>
<code>{Builder.lf_beautify(escape(code))}</code>
        '''

    def code_handler(self, zip_archive: bytes) -> tuple:
        box = str(int(datetime.now().timestamp()))

        root_path = path.join('/tmp', self.token)
        file_path = path.join(root_path, box + '.zip')

        if not path.exists('/tmp/'):
            makedirs(root_path)

        with zipfile.ZipFile(io.BytesIO(zip_archive), 'r') as _zip:
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
                    return False, f'Not a .java file: {file}'

        code_blocks = []

        pic_num = 0

        for root, dirs, files in walk(file_path):
            for file in files:
                for block in self.__get_objects_from_java(path.join(root, file)):
                    code_blocks.append(self.create_code_block(description=f'Рис {pic_num}',
                                                              code=block
                                                              ))
                    pic_num += 1

        return code_blocks


    def __get_objects_from_java(self, code: str) -> list:
        regex = r"(((|public|final|abstract|private|static|protected)(\s+))?(class)(\s+)(\w+)(<.*>)?(\s+extends\s+\w+)?(<.*>)?(\s+implements\s+)?(.*)?(<.*>)?(\s*))\{$(\s.*)+\}"

        matches = re.finditer(regex, code, re.MULTILINE)

        result = []

        for matchNum, match in enumerate(matches, start=1):
            result.extend(match.group())

        return result