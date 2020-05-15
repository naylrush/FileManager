
from django.shortcuts import render
from navigation_files.settings import BASE_DIR
import os


class File:
    def __init__(self, name, is_dir):
        self.name = name
        self.is_dir = is_dir


def open_dir(request, path: str):
    """
    Opens directory by path and returns its own files and directories
    """
    # links '.' and '..' are included to django (I think)
    path = os.path.join(BASE_DIR, path)

    files = [File(file, os.path.isdir(os.path.join(path, file))) for file in os.listdir(path)]
    files.sort(key=lambda file: file.name)

    return render(request, 'navigation/index.html', context={'files': files})


def open_file(request, path: str):
    """
    Opens text file in UTF-8
    """
    with open(path, 'r') as file:
        content = file.read(os.stat(path).st_size)
    return render(request, 'navigation/index.html', context={'content': content})
