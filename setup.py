# -*- coding: utf-8 -*-
"""Setup per la llibreria de cchloader"""
from __future__ import print_function

import os
import shutil
from distutils.command.clean import clean as _clean
from setuptools import setup, find_packages


readme = open("README.md").read()

with open('requirements.txt', 'r') as f:
    INSTALL_REQUIRES = f.readlines()

with open('requirements-dev.txt', 'r') as f:
    TESTS_REQUIRE = f.readlines()


class Clean(_clean):
    """Eliminem el directory build i els bindings creats."""

    def run(self):
        """Comença la tasca de neteja."""
        _clean.run(self)
        if os.path.exists(self.build_base):
            print("Cleaning {} dir".format(self.build_base))
            shutil.rmtree(self.build_base)

setup(
    name='cchloader',
    version='0.4.11',
    packages=find_packages(),
    url='https://github.com/Som-Energia/cchloader',
    license='GPLv3',
    author='Som Energia SCCL',
    author_email='info@somenergia.coop',
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
    tests_require=TESTS_REQUIRE,
    cmdclass={'clean': Clean},
    test_suite='tests',
    provides=['cchloader'],
)
