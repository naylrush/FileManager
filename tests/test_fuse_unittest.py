
try:
    from .config import Config
except ImportError:
    from config import Config

config = Config()  # helps load fuse_system module

from time import sleep
import os
import signal
import subprocess

from fuse_main import run_fuse, umount
from file_tree import FileTree
from file import File


class FuseProcess:
    process = None

    def run(self):
        self.process = subprocess.Popen(['python', '{}/fuse_main.py'.format(config.FILE_SYSTEM), config.FUSE_ROOT,
                                         '--dir', config.SOURCE_DIR])

    def stop(self):
        self.process.send_signal(signal.SIGINT)


def read(path):
    with open(path, 'r') as file:
        return file.read(os.stat(path).st_size)


class TestRunFuse:
    fuse_process = FuseProcess()

    @classmethod
    def setup_class(cls):
        cls.fuse_process.run()
        sleep(0.5)

    def test_run(self):
        pass

    def test_tree(self):
        assert FileTree(config.SOURCE_DIR) == FileTree(config.FUSE_ROOT)

    def test_read(self):
        for value in FileTree(config.SOURCE_DIR).files.values():
            if isinstance(value, File):
                local_file_path = value.real_path[len(config.SOURCE_DIR) + 1:]
                assert read(os.path.join(config.SOURCE_DIR, local_file_path)) == \
                       read(os.path.join(config.FUSE_ROOT, local_file_path))

    @classmethod
    def teardown_class(cls):
        cls.fuse_process.stop()


if __name__ == '__main__':
    test = TestRunFuse()
    test.setup_class()
    test.test_run()
    test.test_tree()
    test.test_read()
    test.teardown_class()
