Flask-PonyWhoosh
================

This is a package to integrate the amazing power of ``Whoosh`` with
``Pony ORM`` inside the ``Flask``.

Running the App
---------------

Nowadays, you should download the repository and where you locate in the
directory. See inside the ``app.py`` and ``entidades.py`` how it works.

.. code:: bash

        pip install virtualenv
        virtualenv --no-site-packages venv
        source venv/bin/activate
        pip install -r requirements.txt
        python app.py runserver

After that, you could visit the following urls. -
``http://localhost:5000/llenar`` - ``http://localhost:5000/update`` -
``http://localhost:5000/`` to see the entities from database.

Searching
---------

.. code:: python

        >>> from entidades import *
        >>> from flask_ponywhoosh import search
        >>> search(User, 'jona')
        <Top 2 Results for Or([<_NullQuery>, Wildcard('name', u'*jona*')]) runtime=0.003
    22508811951>

