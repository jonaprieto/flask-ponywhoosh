'''

  flask_ponywhoosh extension
  ~~~~~~~~~~~~~~~~~~~~~~~~~~

  Perform full-text searches over your database with Pony ORM and PonyWhoosh,
  for flask applications.

  :copyright: (c) 2015-2018 by Jonathan Prieto-Cubides & Felipe Rodriguez.
  :license: MIT (see LICENSE.md)

'''

from __future__ import absolute_import, print_function


import io
import os
import re

from glob       import glob
from os.path    import basename, dirname, join, relpath, splitext
from setuptools import find_packages, setup

def read(*names, **kwargs):
  return io.open(
      join(dirname(__file__), *names)
    , encoding=kwargs.get('encoding', 'utf8')
  ).read()

setup(
    name='flask-ponywhoosh'
  , version="1.0.8"
  , url='https://github.com/jonaprieto/flask-ponywhoosh'
  , license='MIT'
  , author='Jonathan Prieto-Cubides & Felipe Rodriguez'
  , author_email='jprieto9@eafit.edu.co'
  , description='A search engine for Flask using Pony ORM and Whoosh.'
  , long_description='%s' % (read('README.rst'))
  , packages=['flask_ponywhoosh']
  , zip_safe=False
  , include_package_data=True
  , package_data = {'flask_ponywhoosh': ['README.md', 'example.py', 'test.py']}
  , platforms='any'
  , keywords=
    [ 'elastic'
    , 'engine'
    , 'flask'
    , 'flask-sqlalchemy'
    , 'flask-whooshalchemy'
    , 'mysql'
    , 'pony'
    , 'ponyorm'
    , 'ponywhoosh'
    , 'search'
    , 'searchengine'
    , 'searchable'
    , 'sqlite3'
    , 'whoosh'
    ]
  , install_requires=
    [ 'flask-bootstrap'
    , 'flask-wtf'
    , 'ponywhoosh'
    , 'flask'
    , 'flask-script'
    ]
  ,  classifiers=
    [ 'Environment :: Web Environment'
    , 'Intended Audience :: Developers'
    , 'License :: OSI Approved :: MIT License'
    , 'Operating System :: OS Independent'
    , 'Programming Language :: Python'
    , 'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    , 'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
