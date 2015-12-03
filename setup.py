'''

    flask_ponywhoosh extension
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Perform full-text searches over your database with Pony ORM and PonyWhoosh,
    for flask applications.

    :copyright: (c) 2015-2016 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
    :license: BSD (see LICENSE.md)

'''

from __future__ import absolute_import, print_function

from glob import glob
import os
from os.path import basename, dirname, join, relpath, splitext
import re

import io
from setuptools import find_packages, setup



def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

setup(
    name='Flask-PonyWhoosh',
    version="0.2",
    url='https://github.com/compiteing/Flask-PonyWhoosh',
    license='BSD',
    author='Jonathan S. Prieto. & Ivan Felipe Rodriguez',
    author_email='prieto.jona@gmail.com',
    description='Perform your full-text searches on your database. Pony and Whoosh with Flask. All in one.',
    long_description='%s\n%s' % (
        read('README.rst'), re.sub(':obj:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    packages =find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    keywords=['flask', 'pony', 'whoosh', 'ponywhoosh', 'search', 'full-text', 'elastic', 'engine', 'searchable'],
    install_requires=['flask', 'ponywhoosh', 'flask-bootstrap', 'flask-wtf'],
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
# python setup.py build_sphinx
# python setup.py upload_sphinx