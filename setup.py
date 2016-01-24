#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    buf = open(os.path.join(os.path.dirname(__file__), fname), 'rb').read()
    return buf.decode('utf8')


setup(name='jinja-vanish',
      version='0.2.dev1',
      description='Customizable auto-escaping for jinja2.',
      long_description=read('README.rst'),
      author='Marc Brinkmann',
      author_email='git@marcbrinkmann.de',
      url='https://github.com/mbr/jinja-vanish',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      install_requires=['jinja2'],
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ])
