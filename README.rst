.. image:: https://github.com/jonaprieto/flask-ponywhoosh/blob/master/docs/_static/logo.png?raw=true
   :target: https://pypi.python.org/pypi/flask-ponywhoosh
   :scale: 100%
   :align: center
   :alt: PonyWhoosh

flask-ponywhoosh
================
|PyPI Package latest release| |Test|

Get a search engine in your flask application using Pony ORM and Whoosh. 
We included some templates to render the search engine.

Install
-------

.. code:: bash

    $ pip install flask-ponywhoosh

The hard way:

.. code:: bash

    $ git clone https://github.com/jonaprieto/flask-ponywhoosh.git
    $ cd flask-ponywhoosh
    $ python setup.py install

Example
--------

After installing the package. You can clone this repository in order to run the
example or just download the source.

.. code:: bash

    $ git clone https://github.com/jonaprieto/flask-ponywhoosh.git
    $ cd flask-ponywhoosh

Then, you can run the example using:

.. code:: bash

    python example.py runserver

You will see in the shell some outputs showing settings of flask-ponywhoosh (debug mode is on by default).
We provide two urls by default:


    -  `localhost/search` : the form of the search engine
    -  `localhost/database` : contents of the database for our example

Recall `localhost` is usually `http://127.0.0.1:5000`.

Hacking
-------

Customize the templates, URL routes and other stuffs, please
checkout the documentation on:

    -  http://pythonhosted.org/flask-ponywhoosh/
    -  https://pypi.python.org/pypi/flask-ponywhoosh


Screenshots
-----------

Adding what fields of your models in your database you want to search.

.. image:: https://github.com/jonaprieto/flask-ponywhoosh/blob/master/images/databaseconfig.gif?raw=true
   :target: https://pypi.python.org/pypi/flask-ponywhoosh
   :scale: 60%
   :align: center
   :alt: PonyWhoosh




.. image:: http://g.recordit.co/6MnvKNod6y.gif
   :target: https://pypi.python.org/pypi/flask-ponywhoosh
   :scale: 25%
   :align: center
   :alt: PonyWhoosh



.. |PyPI Package latest release| image:: http://img.shields.io/pypi/v/flask-ponywhoosh.png?style=flat

.. |Test| image:: https://travis-ci.org/jonaprieto/flask-ponywhoosh.svg?branch=master
    :target: https://travis-ci.org/jonaprieto/flask-ponywhoosh
