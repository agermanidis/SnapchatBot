#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='snapchat_bots',
    version='0.1',
    description='Library for building Snapchat bots',
    long_description=open('README.md').read(),
    author='Anastasis Germanidis',
    author_email='agermanidis@gmail.com',
    url='https://github.com/agermanidis/SnapchatBot',
    packages=['snapchat_bots'],
    install_requires=[
        'schedule>=0.3.1',
        'requests>=2.5.1',
        'PIL>=1.1.7',
        'pysnap>=0.1.1'
    ],
    dependency_links = ['https://github.com/martinp/pysnap/tarball/master#egg=pysnap-0.1.1'],
    license=open('LICENSE').read()
)
