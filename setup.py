# -*- coding: utf-8 -*-
"""Setup per la llibreria de cchloader"""

import os
from setuptools import setup, find_packages

readme = open("README.md").read()

with open('requirements.txt', 'r') as f:
    INSTALL_REQUIRES = f.readlines()

setup(
    name='cchloader',
    version='0.4.9',
    packages=find_packages(),
    url='https://github.com/Som-Energia/cchloader',
    license='GPLv3',
    author='',
    author_email='',
    long_description=readme,
    long_description_content_type='text/markdown',
    description='''Implementation based on sippers from GISCE
    https://github.com/gisce/sippers''',
    entry_points='''
        [console_scripts]
        usmartdata=usmartdata.cli:usmartdata
    ''',
    package_data={
        'cchloader': ['data/*']
    },
    install_requires=INSTALL_REQUIRES,
    test_suite='tests',
)
