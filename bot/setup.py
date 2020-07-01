#!/usr/bin/env python

from setuptools import setup
from elbb.meta import VERSION

setup(
    name='elbb',
    packages=[
        'elbb',
        'elbb.images'
    ],
    package_data = {
        'elbb.images': ['*.png']
    },
    version=VERSION,
    description='beep boop',
    license='Unlicense',
    url='https://github.com/vesche/elbb',
    author='Austin Jackson',
    author_email='vesche@protonmail.com',
    entry_points={
        'console_scripts': [
            'elbb = elbb.server:start',
        ]
    },
    install_requires=[
        'filelock',
        'numpy',
        'pyautogui',
        'pytesseract',
        'sanic',
        'scipy'
    ],
    classifiers=[
        'License :: Public Domain',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8'
    ]
)