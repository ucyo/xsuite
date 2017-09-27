#!/usr/bin/env python
# coding: utf-8
"""Minimal setup."""

from setuptools import setup, find_packages
import os
import re

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


def get_property(prop, project):
    with open(os.path.join(project, '__init__.py')) as f:
        result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
                           f.read())
    return result.group(1)


project = 'xsuite'
setup(name=project,
      install_requires=requirements,
      version=get_property('__version__', project),
      description='Several extensions for xarray',
      package_data={project:['data/*']},
      author='Ugur Cayoglu',
      tests_require=['pytest >= 3.1.2'],
      author_email='urcyglu@gmail.com',
      # url='',
      packages=find_packages(),
      )
