
from file_system.fuse_main import run_fuse, umount
from navigation_files.settings import SOURCE_DIR, FUSE_ROOT
import signal
import threading


def signal_handler(signum, frame):
    umount(FUSE_ROOT)
    exit(0)


def run_fuse_in_new_thread():
    fuse_thread = threading.Thread(target=run_fuse, args=(FUSE_ROOT, SOURCE_DIR))
    fuse_thread.setDaemon(True)
    fuse_thread.start()


run_fuse_in_new_thread()
signal.signal(signal.SIGINT, signal_handler)
