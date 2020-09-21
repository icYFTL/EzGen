from os import path
from sys import platform
from core import config


def get_static_image(image_name: str):
    raise NotImplementedError
    # return open(path.join('source/static/images', image_name))


def define_tmp_path():
    if platform == "win32":
        return config['windows_path']
    return config['linux_path']
