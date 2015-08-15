Flask-PonyWhoosh
================

This is a package to integrate the amazing power of ``Whoosh`` with
``Pony ORM`` inside the ``Flask``.

Installation
------------

.. code:: python


        pip install flask-ponywhoosh

Usage
-----

Import the library where you define your Entities.

.. code:: python

        from flask_ponywhoosh import Whoosh
        wh = Whoosh()

And for each entity wrapped it with the decorator
``@wh.register_model(*args,**kw)`` like the following example:

.. code:: python

    @wh.register_model('name','edad',sortable=True,  stored=True)
    class User(db.Entity):
        _table_ = 'User'
        id = PrimaryKey(int, auto=True)
        name = Required(unicode)
        tipo = Optional(unicode)
        edad = Optional(unicode)
        entries = Set("Entry")
        atributos = Set("Atributos")

As you see from above example, you should write as strings the fields
that they are going to be searchables, and you can add the parameters
for fields.

Parameters for Flask Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From flask configuration, you could add option for whoosh:

.. code:: python

        app.config['WHOOSHEE_DIR'] = 'whooshes'
        app.config['WHOSHEE_MIN_STRING_LEN'] = 3
        app.config['WHOOSHEE_WRITER_TIMEOUT'] = 2

``PonyModel._whoosh_search_(query, **kwargs)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To execute a search, choose the entity of interest and then, try
something like the following code over a view function, or even from the
shell.

.. code:: python

        >>> from entidades import *
        >>> User._whoosh_search_("felipe")
        {'runtime': 0.002643108367919922, 'results': [User[12], User[5]]}
        >>> from flask_ponywhoosh import search
        >>> search(User,"felipe")
        {'runtime': 0.0016570091247558594, 'results': [User[12], User[5]]}
        >>> search(User,"felipe",sortedby="edad")
        {'runtime': 0.0015339851379394531, 'results': [User[12], User[5]]}
        >>> search(User,"harol",sortedby="edad")
        {'runtime': 0.0038590431213378906, 'results': [User[13], User[6], User
        [14], User[7]]}
        >>>

Usage from Example:
-------------------

-  ``app.py`` for running the flask app.
-  ``entidades.py`` where we defined the entities of database for
   ``PonyORM``.

Running the App
~~~~~~~~~~~~~~~

.. code:: bash

        pip install virtualenv
        virtualenv --no-site-packages venv
        source venv/bin/activate
        pip install -r requirements.txt
        python app.py runserver

After that, you could visit the following urls. -
``http://localhost:5000/llenar`` to create entries for database,
examples. - ``http://localhost:5000/update`` to perform an update in an
entity with ``id=1``. - ``http://localhost:5000/`` to see the entities
from database.

Using the example
~~~~~~~~~~~~~~~~~

Start a session of a shell.

.. code:: bash

        python app.py shell

Try something like the following sentences:

.. code:: python

        >>> from entidades import User
        >>> from flask_ponywhoosh import search
        >>> search(User, 'jona')
