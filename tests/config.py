
import os
import sys


class Config:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(CURRENT_DIR)

    SOURCE_DIR = os.path.join(CURRENT_DIR, 'source_dir')
    FUSE_ROOT = os.path.join(CURRENT_DIR, 'fuse')

    FILE_SYSTEM = os.path.join(BASE_DIR, 'file_system')

    def __init__(self):
        sys.path.append(self.FILE_SYSTEM)

