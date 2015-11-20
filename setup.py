"""
Flask-PonyWhoosh
-------------

Whoosh extension to Flask/PonyORM
"""

from __future__ import absolute_import, print_function

import io
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext
from __version__ import __version__
from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

setup(
    name='Flask-PonyWhoosh',
    version=__version__,
    url='https://github.com/piperod/Flask-PonyWhoosh',
    license='BSD',
    author='Jonathan S. Prieto. & Ivan Felipe Rodriguez',
    author_email='prieto.jona@gmail.com',
    description='Flask Pony Whoosh all in one. Perform your full text search.',
    long_description='%s\n%s' % (
        read('README.rst'), re.sub(':obj:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    py_modules=['flask_ponywhoosh'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    keywords=['flask', 'pony', 'whoosh', 'search'],
    install_requires=[x.strip() for x in
        open(os.path.join(os.path.dirname(__file__),
            'requirements.txt'))],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

# pandoc --from=rst --to=rst --output=README.rst README.rst
# Pasos para subir a pypi
# git tag v...
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi