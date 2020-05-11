
import logging
from errno import EIO, ENOENT, EROFS, EACCES
from stat import S_IFDIR, S_IFREG
# from time import time
# import fcntl
from fuse import FuseOSError, LoggingMixIn, Operations
from file_tree import FileTree
from file import File

# NOW = time()


class FuseConstants:
    DIR_ATTRS = {
        'st_mode': (S_IFDIR | 0o555),
        'st_nlink': 2
    }
    FILE_ATTRS = {
        'st_mode': (S_IFREG | 0o444),
        'st_nlink': 1
    }


class File:
    def __init__(self):
        self.size = 0


class FuseOperations(LoggingMixIn, Operations):
    def __init__(self, mount, source_dir=None):
        self.mount = mount
        if source_dir is None:
            self.files = {'a': {'b': File()},
                          'c': File()
                          }

    def find_file(self, path):
        if path == '/':
            return self.files
        path = path[1:].split('/')
        subdir = self.files
        for dir_ in path:
            subdir = subdir.get(dir_, None)
            if subdir is None:
                return None
        return subdir

    def readdir(self, path, fh):
        in_dir = self.find_file(path)
        if in_dir is None:
            raise FuseOSError(EROFS)
        return ['.', '..'] + list(in_dir.keys())

    def getattr(self, path, fh=None):
        file = self.find_file(path)
        if file is None:
            raise FuseOSError(ENOENT)
        if isinstance(file, dict):
            return FuseConstants.DIR_ATTRS
        else:
            attrs = FuseConstants.FILE_ATTRS
            attrs['st_size'] = file.size
            return attrs
