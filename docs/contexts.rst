.. _contexts:
=================
App Full Example
=================

-  ``app.py`` for running the flask app.


Running the App
***************************************

.. code:: bash

    pip install virtualenv
    virtualenv --no-site-packages venv
    source venv/bin/activate
    pip install -r requirements.txt
    python app.py runserver

After that, you could visit the following urls.

-  ``http://localhost:5000/fixtures`` to create entries for database
   examples.
-  ``http://localhost:5000/update`` to perform an update in an entity
   with ``id=1``.
-  ``http://localhost:5000/`` to see the entities from database.
- ``http://localhost:500/ponywhoosh`` to load the visual  interface. 

Running the app example
***************************************

Start a session of a shell.

.. code:: bash

    python app.py shell

Try something like the following sentences:

.. code:: python

    >>> from app import *
    >>> from flask_ponywhoosh import full_search
    >>> full_search(wh,"ch")
    { 'matched_terms': {'name': ['chuck'], 
                        'deporte': ['chulo', 'lucha']}, 
      'runtime': 0.0033812522888183594  
      'results': {'User': {'items': [User[15], User[8], 
                    User[1]],     
      'matched_terms': {'name': ['chuck']}}, 
      'Attributes': {'items': [Attributes[17], 
                    Attributes[14],         
                    Attributes[11], Attributes[8], 
                    Attributes[5], Attributes[2]],
     'matched_terms': {'deporte': ['chulo', 'lucha']}}
                 }}
