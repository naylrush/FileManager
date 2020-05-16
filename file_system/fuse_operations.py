
from errno import ENOENT, EROFS, EACCES
from file import File
from file_tree import FileTree
from fuse import FuseOSError, LoggingMixIn, Operations
from stat import S_IFDIR, S_IFREG
import os


class FuseConstants:
    DIR_ATTRS = {
        'st_mode': (S_IFDIR | 0o555),
        'st_nlink': 2
    }
    FILE_ATTRS = {
        'st_mode': (S_IFREG | 0o444),
        'st_nlink': 1
    }


class FuseOperations(LoggingMixIn, Operations):
    use_ns = True

    def __init__(self, mount, source_dir=None):
        self.mount = mount
        self.files = FileTree(source_dir)

    def access(self, path, mode):
        file = self.files[path]
        if isinstance(file, File):
            if not os.access(file.real_path, mode):
                raise FuseOSError(EACCES)

    def open(self, path, flags):
        file = self.files[path]
        return os.open(file.real_path, os.O_RDONLY)

    def read(self, path, size, offset, fd):
        os.lseek(fd, offset, 0)
        return os.read(fd, size)

    def release(self, path, fd):
        os.close(fd)

    def readdir(self, path, fd):
        in_dir = self.files[path]
        if in_dir is None:
            raise FuseOSError(EROFS)
        return ['.', '..'] + list(in_dir.keys())

    def getattr(self, path, fd=None):
        file = self.files[path]
        if file is None:
            raise FuseOSError(ENOENT)
        if isinstance(file, dict):
            return FuseConstants.DIR_ATTRS
        attrs = FuseConstants.FILE_ATTRS
        attrs["st_size"] = file.size()
        return attrs
