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

    git clone https://github.com/piperod/flask-ponywhoosh.git



Flask-App Configuration
***********************

|appconfig|

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


Database Configuration
**********************

|database|

Import the Flask_ponywhoosh library in the file you have the database entities.

.. code:: python

    from flask_ponywhoosh import Whoosh
    pw = Ponywhoosh()

For each entity wrap it up with the decorator
``@pw.register_model(*args,**kw)``. Specifying what attributes would be searcheables. For example:

.. code:: python

    @pw.register_model('name','age', sortable=True,  stored=True)
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

The first field you register (in the example, 'name'), would be the main field for you. In that way when you render the template '/ponywhoosh', the cards results would show this field as the main one.

Searching: for the first  time
******************************

|first|

In the shell view you can search using the "search()" function. Running our example, let us suppose  we are looking for the word "applied" in the model Department. After we run our example.py with the shell, we should follow the following steps:


.. |appconfig| image:: https://github.com/jonaprieto/flask-ponywhoosh/blob/master/images/flaskappconfig.gif?raw=true
   :target: https://pypi.python.org/pypi/flask-ponywhoosh

.. |database| image:: https://github.com/jonaprieto/flask-ponywhoosh/blob/master/images/databaseconfig.gif?raw=true
   :target: https://pypi.python.org/pypi/flask-ponywhoosh

.. |first| image:: https://github.com/jonaprieto/flask-ponywhoosh/blob/master/images/searchfirsttime.gif?raw=true
   :target: https://pypi.python.org/pypi/flask-ponywhoosh

