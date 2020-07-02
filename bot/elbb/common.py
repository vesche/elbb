"""elbb.common"""

import os

pwd = os.path.abspath(os.path.dirname(__file__))


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
