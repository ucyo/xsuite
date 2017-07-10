#!/usr/bin/env python
# coding: utf-8
"""Minimal setup."""

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '0.2'

setup(name='xsuite',
      install_requires=requirements,
      version=version,
      description='Several extensions for xarray',
      author='Ugur Cayoglu',
      author_email='urcyglu@gmail.com',
      # url='',
      packages=find_packages(),
      )
