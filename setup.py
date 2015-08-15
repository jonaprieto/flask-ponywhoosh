"""
Flask-PonyWhoosh
-------------

Whoosh extension to Flask/PonyORM
"""

from setuptools import setup
import os


setup(
    name='Flask-PonyWhoosh',
    version='0.1.0',
    url='https://github.com/piperod/Flask-PonyWhoosh',
    license='BSD',
    author='Jonathan S. Prieto. & Ivan Felipe Rodriguez',
    author_email='prieto.jona@gmail.com',
    description='Whoosh extension to Flask/PonyORM',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    py_modules=['flask_ponywhoosh'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
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
    ]
)