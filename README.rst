Welcome to Flask-PonyWhoosh's Source Code Repository!
=====================================================

|PyPI Package latest release| |PyPI Package monthly downloads| |Test|

This package integrate the amazing power of ``Whoosh`` with ``Pony ORM``
inside ``Flask``. Source code and issue tracking at
http://github.com/compiteing/Flask-PonyWhoosh.

Please take a look to the official documentation up-date:
    -  http://pythonhosted.org/Flask-PonyWhoosh/
    -  https://pypi.python.org/pypi/Flask-PonyWhoosh

Installation
------------

.. code:: python

    pip install flask-ponywhoosh

or

.. code:: bash

    git clone https://github.com/compiteing/Flask-PonyWhoosh.git

What's new? 0.1.6
-----------------

We've decided to go one step forward. We wanted have ready for you a
default view and a template where you can actually search and see the
results in a pretty organized way. So right now the parametrizable route
'/ponywhoosh' would let you search in a visual interactive interface!

The basic search form: |Search|

One of two possible ways to view the results is: |Results|

For other updates, see ``CHANGELOG.rst``.

.. |PyPI Package latest release| image:: http://img.shields.io/pypi/v/Flask-PonyWhoosh.png?style=flat
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh
.. |PyPI Package monthly downloads| image:: http://img.shields.io/pypi/dm/Flask-PonyWhoosh.png?style=flat
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh
.. |Test| image:: https://travis-ci.org/piperod/Flask-PonyWhoosh.svg?branch=master
   :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
.. |Search| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/searchform.png?raw=true%0A%20:align%20center%0A%20:height%20400px
.. |Results| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/results.png?raw=true%0A%20:align%20center%0A%20:height%20400px
