

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


If you want the items shown as a list rather than a dictionary. You can use the option use_dict: this option by default is set True. However if you choose false, results will look something like ('field', 'result')
  