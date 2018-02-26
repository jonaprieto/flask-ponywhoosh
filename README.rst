|PonyWhoosh|

flask-ponywhoosh
================

|PyPI Package latest release| |Test|

It's the easiest way to add a search engine in your flask application on
the shoulders of Pony ORM and Whoosh. To prove this, we've included some
templates to render the search engine. Just checkout the example.

Install
-------

-  The natural way:

.. code:: bash

    $ pip install flask-ponywhoosh

-  Using the source:

.. code:: bash

    $ git clone https://github.com/jonaprieto/flask-ponywhoosh.git
    $ cd flask-ponywhoosh

If you are using python 2:

.. code:: bash

    $ make install-py2

If you are using python 2:

.. code:: bash

    $ make install-py3

A small example
---------------

Download the source of this package:

.. code:: bash

    $ git clone https://github.com/jonaprieto/flask-ponywhoosh.git
    $ cd flask-ponywhoosh

Then, you can run the example running these commands:

.. code:: bash

    $ pip install -r requirements.txt
    $ python example.py runserver

You will see in the shell some outputs showing settings of
flask-ponywhoosh (debug mode is on by default). We provide two urls by
default:

    -  <localhost>/ : the form of the search engine
    -  <localhost>/database : raw content of the test database

<localhost> is often http://127.0.0.1:5000.

Hacking
-------

Customize the templates, URL routes and other stuffs, please checkout
the documentation on:

    -  http://pythonhosted.org/flask-ponywhoosh/
    -  https://pypi.python.org/pypi/flask-ponywhoosh

Screenshots
-----------

Adding what fields of your models in your database you want to search.

|PonyWhoosh1|

|PonyWhoosh2|

.. |PonyWhoosh| image:: https://github.com/jonaprieto/flask-ponywhoosh/blob/master/docs/_static/logo.png?raw=true
   :class: align-center
   :target: https://pypi.python.org/pypi/flask-ponywhoosh
.. |PyPI Package latest release| image:: http://img.shields.io/pypi/v/flask-ponywhoosh.png?style=flat
.. |Test| image:: https://travis-ci.org/jonaprieto/flask-ponywhoosh.svg?branch=master
   :target: https://travis-ci.org/jonaprieto/flask-ponywhoosh
.. |PonyWhoosh1| image:: https://github.com/jonaprieto/flask-ponywhoosh/blob/master/images/databaseconfig.gif?raw=true
   :class: align-center
   :target: https://pypi.python.org/pypi/flask-ponywhoosh
.. |PonyWhoosh2| image:: http://g.recordit.co/6MnvKNod6y.gif
   :class: align-center
   :target: https://pypi.python.org/pypi/flask-ponywhoosh
