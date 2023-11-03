from setuptools import setup, find_packages

readme = open("README.md").read()

setup(
    name='cchloader',
    version='0.4.5',
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
    install_requires=[
        "raven",
        "pymongo<3.0",
        "osconf",
        "marshmallow>=2.13.5",
        "click",
        "pytz",
        "psycopg2-binary"
    ],
    test_suite='tests',
)
