#encoding: utf-8
import os
import re
from setuptools import setup, find_packages

# parse version from xdiff/__init__.py
with open(os.path.join(os.path.dirname(__file__), 'xdiff', '__init__.py')) as f:
    version = re.compile(r"__version__\s+=\s+'(.*)'", re.I).match(f.read()).group(1)

with open('README.md') as f:
    long_description = f.read()

setup(
    name='xdiff',
    version=version,
    description='A CLI tool to compare data structures, files, folders, http responses, etc.',
    long_description=long_description,
    author='Leo Lee',
    author_email='mail@debugtalk.com',
    url='https://github.com/debugtalk/xdiff.git',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'termcolor',
        'PyYAML',
        'future'
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'xdiff=xdiff.cli:main'
        ]
    }
)
