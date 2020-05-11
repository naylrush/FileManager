
from fuse import FUSE
from fuse_operations import FuseOperations
import argparse
import logging


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mount')
    # Not implemented
    parser.add_argument('--dir', dest='source_dir', default=None)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    FUSE(FuseOperations(args.mount, args.source_dir), args.mount,  foreground=True, allow_other=True)
