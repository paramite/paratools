# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='paratools',
    version='0.1',
    author='Martin Magr',
    author_email='martin.magr@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'tkn = paratools.tkn:tkn',
            'vmip = paratools.vmip:vmip',
            'vmprep = paratools.vmprep:vmprep',
            'vmclone = paratools.vmclone:vmclone',
        ],
    }
)
