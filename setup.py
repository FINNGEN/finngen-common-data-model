#!/usr/bin/env python
from distutils.core import setup

setup(name='finngen_common_data_model',
      version='0.0.1',
      description='finngen common data model',
      author='major seitan',
      packages=['finngen_common_data_model'],
      license='MIT',
      url='https://github.com/FINNGEN/finngen-common-data-model',
      package_dir={ 'finngen_common_data_model': 'finngen_common_data_model' },
      install_requires=[ 'attrs>=19.3.0',
                         'SQLAlchemy>=1.3.18',
                         'pytest>=5.4.3' ])
