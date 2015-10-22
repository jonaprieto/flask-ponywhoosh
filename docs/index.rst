Welcome to Flask-PonyWhoosh's documentation!
============================================

|PyPI Package latest release| |PyPI Package monthly downloads| |Test|

This package integrate the amazing power of ``Whoosh`` with ``Pony ORM``
inside ``Flask``. Source code and issue tracking at
http://github.com/piperod/Flask-PonyWhoosh.

============
Installation
============

.. code:: python

    pip install flask-ponywhoosh

or

.. code:: bash

    git clone https://github.com/piperod/Flask-PonyWhoosh.git


=====
Usage
=====

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

As you could see in the previous example, you should declare as strings these fields where you want whoosh to store the searcheables (``name``, ``age``, etc.). All the parameters from whoosh are available you just have to listed, separating them with commas: sortable, stored, scored, etc. Refer to whoosh documentation for
further explanations on the application of these parameters. 
 
=================
What's new? 0.1.5
=================

We decided to go one step forward. We decided to have ready for you a default view and a template where you can actually search and  see the results in a pretty organized way. So right now the route '/ponywhoosh' would let you search and view in a visual interactive interface!

This will be further explained in the bonus section. 

For other updates, see ``CHANGELOG.rst``.

==============
Flask Settings
==============

From a flask configuration, you could add the following options if you want to:

.. code:: python

    app.config['WHOOSHEE_DIR'] = 'whooshes'
    app.config['WHOSHEE_MIN_STRING_LEN'] = 3
    app.config['WHOOSHEE_WRITER_TIMEOUT'] = 2


=========
Searching
=========

.. code :: python
    
   PonyModel._wh_.search(query, **kwargs)

There are several options to perform a search with ``flask_ponywhoosh``. For instance, to execute a  simple search, choose the entity where you want to perform the search and then  try
something like the following code over a view function, or even from the shell,

.. code:: python

  >>> from app import *
  >>> User._wh_.search("felipe")
  {'cant_results': 2,
   'facet_names': [],
   'matched_terms': {'name': ['felipe']},
   'results': [{'docnum': 4L,
                'rank': 0,
                'pk': 5,
                'score': 2.540445040947149},
               {'docnum': 11L,
                'rank': 1,
                'pk': 12,
                'score': 2.540445040947149}],
   'runtime': 0.001981973648071289}

If you would prefer, you may use the function ``search()``,  which will run the same function but is quite more handy when writing

.. code:: python

    >>> from flask_ponywhoosh import search
    >>> from app import *
    >>> search(User,"felipe") 
    {'cant_results': 2,
     'facet_names': [],
     'matched_terms': {'name': ['felipe']},
     'results': [{'docnum': 4L,
                  'rank': 0,
                  'pk' : 5,
                  'score': 2.540445040947149},
                 {'docnum': 11L,
                  'rank': 1,
                  'pk' : 12,
                  'score': 2.540445040947149}],
     'runtime': 0.001981973648071289}

The function ``search()`` takes three arguments.
1. A ponymodel, the databse entity where you want to perform the search.
2. The s``earch_string``, what  you are looking for; and,
3. The arguments, some additional options for more refined searching.

.. code:: python

    search(PonyModel, query, **kw)

For example if  you want  the results to be sorted by some specific searcheable field,
you have to indicate so, by adding the argument ``sortedby="field"``.

In this case the search results object would show as a score the value of the item you choose for sorting. Please note that in order for
one field to be sortable, you must indicate it when you are registering
the model. (Refer to the *Usage* section above)

.. code:: python

    >>> from app import *
    >>> from flask_ponywhoosh import search
    >>> search(User,"harol", sortedby="age")
    {'cant_results': 2,
     'facet_names': [],
     'matched_terms': {'name': ['felipe']},
     'results': [{'docnum': 4L,
                  'rank': 0,
                  'pk' : 5,,
                  'score': '19'},
                 {'docnum': 11L,
                  'rank': 1,
                  'pk' : 12,,
                  'score': '19'}],
     'runtime': 0.0012810230255126953}

In synthesis, the options available are: ``sortedby``, ``scored``, ``limit``, ``optimize``, ``reverse``. Which are widely described in the whoosh documentation.

Searching by field:
*******************

.. code:: python 

    search(PonyModel, query, field="field_name")

By default the function ``search()`` performs a multifield parser query, i.e. that you will be searching in all the fields you have declared when you registered the model. However, sometimes you would like to perform searching in just one or some of all the fields.
For these reasons we implemented the following extra options: The first one is refered as ``field`` all you have to do is indicate in which field you want to search. The output would be a results object containing only the information found in that field. And ``fields`` where you should write a list with all the fields you want to search. 

.. code:: python 

    >>> search(User,"harol",field="name")
         {'cant_results': 4,
         'facet_names': [],
         'matched_terms': {'name': ['harol']},
         'results': [{'docnum': 1L,
                      'pk': u'7',
                      'rank': 0,
                      'score': 2.0296194171811583},
                     {'docnum': 5L,
                      'pk': u'6',
                      'rank': 1,
                      'score': 2.0296194171811583},
                     {'docnum': 12L,
                      'pk': u'13',
                      'rank': 2,
                      'score': 2.0296194171811583},
                     {'docnum': 13L,
                      'pk': u'14',
                      'rank': 3,
                      'score': 2.0296194171811583}],
         'runtime': 0.005359172821044922}

    >>> search(Attribute,"tejo", fields=["sport","name"])
        {'cant_results': 4,
         'facet_names': [],
         'matched_terms': {'name': ['tejo'], 'sport': ['tejo']},
         'results': [{'docnum': 1L,
                      'pk': u'7',
                      'rank': 0,
                      'score': 5.500610730717037},
                     {'docnum': 6L,
                      'pk': u'1',
                      'rank': 1,
                      'score': 5.500610730717037}],
         'runtime': 0.006212949752807617}

The arguments ``add_wildcards`` and ``something``
***************************************************

.. code :: python
    
   search(PonyModel, query, add_wildcards=True)

Whoosh  sets a wildcard ``*``,``?``,``!`` by default to perform search for inexact terms, however sometimes  is desirable to search by exact terms instead. For this reason we added two more options: ``add_wildcards`` and ``something``. 

The option *add_wildcards* (by default False)  is a boolean argument that tells the searcher whether it should or not include wild cards. For example, if you want to search "harol" when ``add_wildcards=False``, and you search by "har" the results would be 0. If ``add_wildcards=True`` , then "har" would be fair enough to get the result "harol"  because searching was performed in using wild cards. 

.. code:: python

        >>> search(User, "har", add_wildcards=False)
          {'cant_results': 0,
           'facet_names': [],
           'matched_terms': {},
           'results': [],
           'runtime': 0.0003230571746826172
           }

        >>> search(User, "har", add_wildcards=True)
          {'cant_results': 4,
           'facet_names': [],
           'matched_terms': {'name': ['harol']},
           'results': [{'docnum': 1L,
                        'pk': u'7',
                        'rank': 0,
                        'score': 2.0296194171811583},
                       {'docnum': 5L,
                        'pk': u'6',
                        'rank': 1,
                        'score': 2.0296194171811583},
                       {'docnum': 12L,
                        'pk': u'13',
                        'rank': 2,
                        'score': 2.0296194171811583},
                       {'docnum': 13L,
                        'pk': u'14',
                        'rank': 3,
                        'score': 2.0296194171811583}],
           'runtime': 0.014926910400390625}

The ``something=True`` option, would run first a search with 
``add_wildcards=False`` value, but in case results are empty it would automatically run a search adding wildcards to the result. 

.. code:: python 

    >>> search(Attribute, "tejo", something = True)
      {'cant_results': 4,
       'facet_names': [],
       'matched_terms': {'name': ['tejo'], 'sport': ['tejo']},
       'results': [{'docnum': 1L,
                    'pk': u'7',
                    'rank': 0,
                    'score': 5.500610730717037},
                   {'docnum': 6L,
                    'pk': u'1',
                    'rank': 1,
                    'score': 5.500610730717037}],
       'runtime': 0.0036530494689941406}
  
======================
The results dictionary
======================

The ``search()`` function returns a dictionary with selected information. 

* ``cant_results``: is the total number of documents collected by the searcher. 
* ``facet_names``: is useful with the option ``groupedby``, because it returns the item used to group the results. 
* ``matched_terms``: is a dictionary that saves the searcheable field and the match given by the query. 
* ``runtime``: how much time the searcher took to find it.   
* ``results``: is  a dictionary's list for the individual results. i.e. a dictionary for every single result, containing: 

  * 'rank': the position of the result, 
  * 'result': indicating the primary key and the correspond value of the item, 
  * 'score': the score for the item in the search, and
  * 'pk': the primary key


  
====================
Full Search Function
====================

.. code :: python
    
  full_search(query, **kwargs)

This function allows you to search in every model instead of searching in one by one. ``full_search`` takes three arguments: ``wh`` is by default the whoosheers where the indexes of  models from the database are stored. ``arg`` is where you type your query, and the last arguments  are the options just as were described before,  with the new feature for ``models`` (this is explained later in this section). 

.. code:: python

    >>> from app import *
    >>> from flask_ponywhoosh import full_search
    >>> full_search(wh,"ch")
    {'cant_results': 6,
     'matched_terms': {'name': ['chuck'], 'sport': ['chulo', 'lucha']},
     'results': {'Attribute': {'items': [{'docnum': 0L,
                                          'pk': u'11',
                                          'rank': 0,
                                          'score': 2.1365658814678095},
                                         {'docnum': 2L,
                                          'pk': u'8',
                                          'rank': 1,
                                          'score': 2.1365658814678095},
                                         {'docnum': 7L,
                                          'pk': u'2',
                                          'rank': 2,
                                          'score': 2.1365658814678095},
                                         {'docnum': 10L,
                                          'pk': u'5',
                                          'rank': 3,
                                          'score': 2.1365658814678095}],
                               'matched_terms': {'sport': ['chulo', 'lucha']}},
                 'User': {'items': [{'docnum': 2L,
                                     'pk': u'8',
                                     'rank': 0,
                                     'score': 2.540445040947149},
                                    {'docnum': 6L,
                                     'pk': u'1',
                                     'rank': 1,
                                     'score': 2.540445040947149}],
                          'matched_terms': {'name': ['chuck']}}},
     'runtime': 0.022469043731689453}
        
The results object for this function is a dictionary containing 'runtime': The sum of the runtime for the search in every field. 'matched_terms': another dictionary that stores the field where the query matched and a list with the results obtained. 'results': A dictionary with the location of every result listed by the field. 


If you would rather prefer, you can indicate specifically in which models are you interested on searching, by indicating in the arguments of the function *full_search(wh,"search_string", models=[list with the models])*. For example:

.. code:: python

        >>> from app import *
        >>> from flask_ponywhoosh import full_search
        >>> full_search(wh,"ch",models=[User])
        

================================
The method ``PonyModel._wh_.``
================================

There are some special features avalaible for models from the database: 


* ``add_field``: This function is to add a desired field in the index. 
* ``charge_documents``: This function let you charge an index from an  existing database. 
* ``delete_documents``: This function deletes all the documents stored in certain whoosh index. 
* ``delete_field``: This function works in case that you want to erase a determined field from a schema. 
* ``update_documents``: This function deletes all the documents and recharges them again. 
* ``counts``: This function counts all the documents existing in an indexes. 

=================
BONUS  :/ponywhoosh ! 
=================

We  aknowledged  that the way we were showing the results was not the most convinient, for this reason we thought that it would be nice and useful to get ready for you a fully interactive and visual interface where you can perform the searches for your own website. So  right now is by  default available at the route '<your_url>/ponywhoosh'. This route looks  something like this. 

|Pony|

These form was made thinking in what is more important (query, fields, add wildcards or something, etc). Then if you submit the search, it would show you the results in a parametrized way, deppending on the name of your tables and wheter they are searcheables or not. 

|Results|

To run this template and make it work, you only have to add to your own route the extension /ponywhoosh  and it would redirect you to the personalized view for your own searches. 

========
Testing
========

Currently we have implemented some basic tests, primary over the ``search()`` and ``full_search()`` functions. You can find them in the file 'test.py'.

In the terminal you have to write the following commands to run the tests:

.. code:: bash 
    
    python -m unittest test

This option  runs all the test and display ``OK``, if all of them were satisfied, the time taken to run all of them and how many were there . 

.. code:: bash 

    python -m unittest -v test

This option displays every test. 
    


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
   

.. |PyPI Package latest release| image:: http://img.shields.io/pypi/v/Flask-PonyWhoosh.png?style=flat
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh
.. |PyPI Package monthly downloads| image:: http://img.shields.io/pypi/dm/Flask-PonyWhoosh.png?style=flat
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh
.. |Test| image:: https://travis-ci.org/piperod/Flask-PonyWhoosh.svg?branch=master
    :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
.. |Pony| image:: https://raw.githubusercontent.com/compiteing/flask-ponywhoosh/master/docs/_static/%3Aponywhoosh.png
    :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
.. |Results| image:: https://raw.githubusercontent.com/compiteing/flask-ponywhoosh/master/docs/_static/results.png
    :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
