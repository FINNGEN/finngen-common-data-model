#!/usr/bin/env python
from distutils.core import setup
setup(name='commons',
      version='1.0',
      description='data commons',
      author='major seitan',
      packages=['commons'],
      install_requires=[ 'attrs>=19.3.0',
                         'SQLAlchemy>=1.3.18',
                         'pytest>=5.4.3' ])
