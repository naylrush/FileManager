
from file import File
import os


def split_path(path):
    if path == '':
        return []
    return path[1 if path[0] == '/' else 0:].split('/')


class FileTree:
    def __init__(self, path=None):
        self.files = {}
        if path is not None:
            self.generate_fs_by(path)

    def add_dir_at(self, path):
        path = split_path(path)
        if len(path) == 0:
            return self.files
        subdir = self.files
        for dir_ in path:
            next_subdir = subdir.get(dir_, None)
            if next_subdir is None:
                next_subdir = subdir[dir_] = {}
            subdir = next_subdir
        return subdir

    def add_file_at(self, path, real_path):
        path, name = os.path.split(path)
        subdir = self.add_dir_at(path)
        subdir[name] = File(real_path)

    def find_file(self, path):
        if path == '/':
            return self.files
        path = split_path(path)
        subdir = self.files
        for dir_ in path:
            subdir = subdir.get(dir_, None)
            if subdir is None:
                return None
        return subdir

    def generate_fs_by(self, path):
        real_root = os.path.realpath(path)
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                # file_real_path = os.path.join(root[len(path) + 1:], name)
                self.add_file_at(os.path.join(root[len(path) + 1:], name), os.path.join(root, name))
            for name in dirs:
                self.add_dir_at(os.path.join(root, name)[len(path):])
