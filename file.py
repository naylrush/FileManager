
import os


class File:
    def __init__(self, real_path):
        self.real_path = real_path

    def size(self):
        return os.path.getsize(self.real_path)
