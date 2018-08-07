#!/usr/bin/env python

from distutils.core import setup

setup(name='iris-data',
      version='1.0',
      description='Iris session data library',
      author='Digirati Ltd',
      py_modules=['iris_data'],
      license='MIT',
      install_requires=[
          'boto3',
          'pytest',
          'moto'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python 3',
          'Programming Language :: Python 3 :: Only',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ]
      )
