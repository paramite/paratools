# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='paratools',
    version='0.1',
    author='Martin Magr',
    author_email='martin.magr@gmail.com',
    py_modules=['paratools'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'vmip = paratools.vmip:vmip',
            'tkn = paratools.tkn:tkn',
        ],
    }
)
