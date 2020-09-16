#!/usr/bin/env python
from distutils.core import setup
setup(name='finngen-common-data-model',
      version='0.0.1',
      description='finngen common data model',
      author='major seitan',
      packages=['finngen-common-data-model'],
      install_requires=[ 'attrs>=19.3.0',
                         'SQLAlchemy>=1.3.18',
                         'pytest>=5.4.3' ])
