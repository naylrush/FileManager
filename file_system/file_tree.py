
try:
    from .file import File
except ImportError:
    from file import File
import os


def split_path(path):
    if path == '':
        return []
    return path[1 if path[0] == '/' else 0:].split('/')


class FileTree:
    def __init__(self, path=None, *, files=None):
        if files is None:
            files = {}
        self.files = files
        if path is not None:
            self.generate_fs_by(path)

    def add_dir_at(self, path):
        path = split_path(path)
        if not path:
            return self.files
        subdir = self.files
        for dir_ in path:
            subdir = subdir.setdefault(dir_, {})
        return subdir

    def add_file_at(self, path, real_path):
        path, name = os.path.split(path)
        subdir = self.add_dir_at(path)
        subdir[name] = File(real_path)

    def find(self, path):
        if path == '/':
            return self.files
        path = split_path(path)
        subdir = self.files
        for dir_ in path:
            subdir = subdir.get(dir_)
            if subdir is None:
                return None
        return subdir

    def __getitem__(self, path):
        return self.find(path)

    def generate_fs_by(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file_real_path = os.path.join(os.path.realpath(root), name)
                self.add_file_at(os.path.join(root[len(path):], name), file_real_path)
            for name in dirs:
                self.add_dir_at(os.path.join(root, name)[len(path):])

    def __str__(self):
        return str(self.files)

    def __eq__(self, other):
        for key, value in self.files.items():
            other_value = other.files.get(key)
            if type(value) == type(other_value):
                if isinstance(value, dict):
                    if FileTree(files=value) != FileTree(files=other_value):
                        return False
            else:
                return False
        return True

    def __ne__(self, other):
        return not self == other
