#encoding: utf-8
import os
import re
from setuptools import setup, find_packages

# parse version from xdiff/__init__.py
with open(os.path.join(os.path.dirname(__file__), 'xdiff', '__init__.py')) as f:
    version = re.compile(r"__version__\s+=\s+'(.*)'", re.I).match(f.read()).group(1)

def load_file(filepath):
    with open(filepath) as f:
        return f.read()

setup(
    name='xdiff',
    version=version,
    description='A CLI tool to compare data structures, files, folders, http responses, etc.',
    long_description=load_file('README.md'),
    author='Leo Lee',
    author_email='mail@debugtalk.com',
    url='https://github.com/debugtalk/xdiff.git',
    license=load_file('LICENSE'),
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'termcolor',
        'PyYAML'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'xdiff=xdiff.cli:main'
        ]
    }
)
