.. _add_wildcars:

The arguments ``add_wildcards`` and ``something``
***************************************************

.. code :: python
    
   search(PonyModel, query, add_wildcards=True)

Whoosh  sets a wildcard ``*``,``?``,``!`` by default to perform search for inexact terms, however sometimes  is desirable to search by exact terms instead. For this reason we added two more options: ``add_wildcards`` and ``something``. 

The option *add_wildcards* (by default False)  is a boolean argument that tells the searcher whether it should or not include wild cards. For example, if you want to search "harol" when ``add_wildcards=False``, and you search by "har" the results would be 0. If ``add_wildcards=True`` , then "har" would be fair enough to get the result "harol"  because searching was performed  using wild cards. 

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