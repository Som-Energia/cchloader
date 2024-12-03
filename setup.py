# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

PACKAGES_DATA = {'cchloader': ['data/*']}

setup(
    name='cchloader',
    version='3.3.2',
    packages=find_packages(),
    url='https://github.com/gisce/cchloader',
    license='GPLv3',
    author='',
    author_email='',
    description='''Implementation based on sippers from GISCE 
    https://github.com/gisce/sippers''',
    entry_points='''
        [console_scripts]
        usmartdata=usmartdata.cli:usmartdata
    ''',
    package_data=PACKAGES_DATA,
    install_requires=requirements,
    test_suite='',
)
