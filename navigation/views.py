
from django.shortcuts import render
import os


BASE_DIR = os.getcwd()


def base(request):
    files = os.listdir(BASE_DIR)
    return render(request, 'navigation/index.html', context={'files': files})


def go(request, path: str):
    if path.endswith('..'):
        path = os.path.basename(path)
    elif path.endswith('.'):
        # do nothing
        path = path[:len(path) - 1]

    path = os.path.join(BASE_DIR, path)
    all_files = os.listdir(path)
    print(all_files)
    files = [f for f in all_files if os.path.isfile(os.path.join(path, f))]
    dirs = set(all_files) ^ set(files)
    print(dirs, files)
    return render(request, 'navigation/index.html', context={'dirs': dirs,
                                                             'files': files,
                                                             'content': None})


def open(request, path: str):
    fd = os.open(path, os.O_RDONLY)
    content = (os.read(fd, os.stat(path).st_size)).decode('utf-8')
    print(content)
    os.close(fd)
    return render(request, 'navigation/index.html', context={'content': content})
