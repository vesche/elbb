"""elbb.cli"""

import os
import bpython
import argparse

from elbb.common import pwd, clear
from elbb.server import start_server
from elbb.meta import BANNER, VERSION


def get_parser():
    parser = argparse.ArgumentParser(description='elbb')
    parser.add_argument(
        '-s', '--server', help='start server',
        default=False, action='store_true'
    )
    parser.add_argument(
        '-i', '--interactive', help='interactive engine mode',
        default=False, action='store_true'
    )
    parser.add_argument(
        '-v', '--version', help='display the current version',
        default=False, action='store_true'
    )
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(VERSION)

    elif args['server']:
        print(BANNER)
        start_server()

    elif args['interactive']:
        clear()
        print('elbb.engine loaded!')
        engine_path = os.path.join(pwd, 'engine.py')
        bpython.embed(args=['-i', '-q', engine_path])

    else:
        parser.print_help()
