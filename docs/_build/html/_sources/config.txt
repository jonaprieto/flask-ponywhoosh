.. _config:
================
Getting Started:
================


Installation
************

.. code:: python

    pip install flask-ponywhoosh

or

.. code:: bash

    git clone https://github.com/piperod/Flask-PonyWhoosh.git



Flask-App Configuration
***********************

In the file you are running  your app, you can initialize the
FlaskPonywhoosh and set up the general configurations. 

.. code :: python
	
	from flask_ponywhoosh import Ponywhoosh
	Ponywhoosh(app) 

.. code:: python

    app.config['WHOOSHEE_DIR'] = 'whooshes'
    app.config['PONYWHOOSH_DEBUG'] = False
    app.config['WHOSHEE_MIN_STRING_LEN'] = 3
    app.config['WHOOSHEE_WRITER_TIMEOUT'] = 2
    app.config['WHOOSHEE_URL'] = '/ponywhoosh'

These configurations set up the default folder to save the Indexes, if you want to activate debug, the minimun lenght of the string in the query, the time out (stop searching if is taking so much) and the route where you might charge the default template for searching (available from version 0.1.5.)


Database Config
***************
Import the Flask_ponywhoosh library in the file you have the database entities.

.. code:: python

    from flask_ponywhoosh import Whoosh
    pw = Whoosh()

For each entity wrap it up with the decorator
``@wh.register_model(*args,**kw)``. Specifying what attributes would be searcheables. For exa:

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

As you could see in the previous example, you should declare as strings these fields where you want whoosh to store the searcheables (``name``, ``age``, etc.). All the parameters from whoosh are available, You just have to listed separating them with commas: sortable, stored, scored, etc. Refer to whoosh documentation for
further explanations on the application of these parameters.
