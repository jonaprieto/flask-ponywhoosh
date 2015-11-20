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


Changelog
=========

0.1.6 (2015-10-20)
-----------------------------------------
* Improvements of Front-End Example Search Page and Results Page
* New contribuitor, alegomezc64 to make the design/js of front pages.

0.1.5 (2015-10-20)
-----------------------------------------
* wh.init_opts(**) depracted
* <your_url>/ponywhoosh
* config constant: WHOOSHEE_URL to add a view of search engine
* config constant:  PONYWHOOSH_DEBUG for debugging purposes
* fix bugs about search arguments and other stuffs.
* full_search now accepts models as strings as wells.
* Please look up into the documentation for more details about this version.



0.1.4 (2015-09-11)
-----------------------------------------
* Add new testing base: test.py
* Add support to search in fields with int, float and datetime type.
* Add include entity in results of search.
* Add pruning for options in search without support.
* Fixed some bugs in app.py (flask example app).
* Optimze the indexes as an method .optimize(), no by default.


0.1.3 (2015-08-29)
-----------------------------------------
* There were several changes, so please refer to documentation to see a complete description. Most of them, they were about new methods for whoosheers and, general methods like full_search, and the way you can perform a search within a entity.


0.1.2 (2015-08-15)
-----------------------------------------
* Add Documentation

0.1.1 (2015-08-15)
-----------------------------------------

* Add a new logo!!!
* Add examples in the documention
* The documentation is now available with Spinix

0.1.0 (2015-08-14)
-----------------------------------------

* First release on PyPI.