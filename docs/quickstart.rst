.. _quickstart:


=========
Searching
=========

.. code :: python
    
   PonyModel._pw_.search(query, **kwargs)

There are several options to perform a search with ``flask_ponywhoosh``. For instance, to execute a  simple search, choose the entity where you want to perform the search and then  try
something like the following code over a view function, or even from the shell,

.. code:: python

  >>> from app import *
  >>> User._pw_.search("felipe")
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

The function ``search()`` takes up to three arguments.
1. A ponymodel, the databse entity where you want to perform the search.
2. The ``search_string``, what  you are looking for; and,
3. The arguments, some additional options for more refined searching.

.. code:: python

    search(PonyModel, "query", **kw)

For example, if  you want  the results to be sorted by some specific searcheable field,
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

By default the function ``search()`` performs a multifield parser query, i.e.  you will be searching in all the fields you have declared when you registered the model. However, sometimes you would like to perform searching in just one or some of all the fields.
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