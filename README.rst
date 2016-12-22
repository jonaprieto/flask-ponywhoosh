Flask-PonyWhoosh
================
|PyPI Package latest release| |Test|

Install package, import it and start adding what fields of your models in
your database you want to search.
We included some templates for the search engine.

Install:
-------

The easiest way:

.. code:: bash

    $ pip install flask-ponywhoosh

The hard way:

.. code:: bash

    $ git clone https://github.com/compiteing/flask-ponywhoosh.git
    $ cd flask-ponywhoosh
    $ python setup.py install

Example:
--------

Clone this repository in order to run the example or just download the source.

.. code:: bash

    $ git clone https://github.com/compiteing/flask-ponywhoosh.git
    $ cd flask-ponywhoosh

Then, you can run the example using:

.. code:: bash

    python example.py runserver

You will see in the shell outputs about the settings of Flask-PonyWhoosh.
We provide two urls by default:

    -  `localhost/search` : the form of the search engine
    -  `localhost/database` : contents of the database for our example

Recall `localhost` is usually `http://127.0.0.1:5000`.

Hacking
-------

Customize the templates, url routes and other stuffs, please
checkout the documentation on:

    -  http://pythonhosted.org/Flask-PonyWhoosh/
    -  https://pypi.python.org/pypi/Flask-PonyWhoosh


Screenshots
-----------

Adding what fields of your models in your database you want to search.

.. image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/images/databaseconfig.gif?raw=true
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh
   :scale: 60%
   :align: center
   :alt: PonyWhoosh



If you want with flask, you can a server and visit a route by default `/ponywhoosh` to the search engine. (you can change it if you need)

.. image:: http://g.recordit.co/6MnvKNod6y.gif
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh
   :scale: 25%
   :align: center
   :alt: PonyWhoosh



.. |PyPI Package latest release| image:: http://img.shields.io/pypi/v/Flask-PonyWhoosh.png?style=flat
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh

.. |Test| image:: https://travis-ci.org/compiteing/flask-ponywhoosh.svg?branch=master
    :target: https://travis-ci.org/compiteing/flask-ponywhoosh
