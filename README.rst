Welcome to Flask-PonyWhoosh's documentation!
============================================

|PyPI Package latest release| |PyPI Package monthly downloads| |Test|

This package integrate the amazing power of ``Whoosh`` with ``Pony ORM``
inside ``Flask``. Source code and issue tracking at
http://github.com/piperod/Flask-PonyWhoosh.

Please take a look to the official documentation up-date: http://pythonhosted.org/Flask-PonyWhoosh/



Installation
------------

.. code:: python

    pip install flask-ponywhoosh

or

.. code:: bash

    git clone https://github.com/piperod/Flask-PonyWhoosh.git

Usage
-----

Import the library where you define your Entities.

.. code:: python

    from flask_ponywhoosh import Whoosh
    wh = Whoosh()

And for each entity wrap it up with the decorator
``@wh.register_model(*args,**kw)``. like the following example:

.. code:: python

    @wh.register_model('name','age', sortable=True,  stored=True)
    class User(db.Entity):
        _table_ = 'User'
        id = PrimaryKey(int, auto=True)
        name = Required(unicode)
        tipo = Optional(unicode)
        age = Optional(int)
        entries = Set("Entry")
        attributes = Set("Attributes")

As you could see in the previous example, you should declare as strings
these fields where you want whoosh to store the searcheables (``name``,
``age``, etc.). All the parameters from whoosh are available, You just
have to listed separating them with commas: sortable, stored, scored,
etc. Refer to whoosh documentation for further explanations on the
application of these parameters.

What's new? 0.1.5
-----------------

We've decided to go one step forward. We wanted have ready for you a
default view and a template where you can actually search and see the
results in a pretty organized way. So right now the parametrizable route
'/ponywhoosh' would let you search in a visual interactive interface!

This will be further explained in the bonus section.

For other updates, see ``CHANGELOG.rst``.



.. |PyPI Package latest release| image:: http://img.shields.io/pypi/v/Flask-PonyWhoosh.png?style=flat
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh
.. |PyPI Package monthly downloads| image:: http://img.shields.io/pypi/dm/Flask-PonyWhoosh.png?style=flat
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh
.. |Test| image:: https://travis-ci.org/piperod/Flask-PonyWhoosh.svg?branch=master
   :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
.. |PonyWhoosh| image:: https://raw.githubusercontent.com/compiteing/flask-ponywhoosh/master/docs/_static/%3Aponywhoosh.png
   :target: https://travis-ci.org/piperod/Flask-PonyWhoosh

