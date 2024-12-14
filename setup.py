#!/usr/bin/env python
import setuptools
from setuptools import find_packages
from setuptools import setup
import re, os

packages = find_packages(exclude=('tests', 'doc'))
provides = ['taurex_catalogue', ]

requires = []

install_requires = ['taurex', 'pytest', 'pandas']

entry_points = {'taurex.plugins': 'catalogue = taurex_catalogue'}

setup(name='taurex_catalogue',
      author="Quentin Changeat, Ahmed Faris Al-Refaie",
      author_email="quentin.changeat.18@ucl.ac.uk",
      license="BSD",
      description='Plugin to automatically load and search planetary and stellar parameters',
      packages=packages,
      entry_points=entry_points,
      provides=provides,
      requires=requires,
      install_requires=install_requires)