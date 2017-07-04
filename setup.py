#!/usr/bin/env python
# coding: utf-8
"""Minimal setup."""

from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '0.1'

setup(name='xsuite',
      install_requires=requirements,
      version=version,
      description='Several extensions for xarray',
      author='Ugur Cayoglu',
      author_email='urcyglu@gmail.com',
      # url='',
      packages=['xsuite'],
      )
