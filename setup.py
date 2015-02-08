#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='snapchat_agents',
    version='0.1',
    description='Library for making Snapchat Agents',
    long_description=open('README.md').read(),
    author='Anastasis Germanidis',
    author_email='agermanidis@gmail.com',
    url='https://github.com/agermanidis/snapchat_agents',
    packages=['snapchat_agents'],
    scripts=['examples/reflector.py', 'examples/storifier.py'],
    install_requires=[
        'pysnap>=0.1.1',
    ],
    license=open('LICENSE').read()
)
