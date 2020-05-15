
from django.shortcuts import render
import os


BASE_DIR = os.getcwd()


def go(request, path: str):
    """
    Opens directory by path and returns its own files and directories
    """
    # links '.' and '..' are included to django (I think)
    path = os.path.join(BASE_DIR, path)
    all_files = os.listdir(path)
    dirs = [dir_ for dir_ in all_files if os.path.isdir(os.path.join(path, dir_))]
    files = set(all_files) ^ set(dirs)
    return render(request, 'navigation/index.html', context={'dirs': dirs,
                                                             'files': files,
                                                             'content': None})


def open(request, path: str):
    """
    Opens text file in UTF-8
    """
    fd = os.open(path, os.O_RDONLY)
    content = (os.read(fd, os.stat(path).st_size)).decode('utf-8')
    os.close(fd)
    return render(request, 'navigation/index.html', context={'content': content})
