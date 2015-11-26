====================
Bonus:/ponywhoosh ! 
====================

We  aknowledged  that  we could do better in how the results were shown, for this reason we thought that it would be nice and useful to get ready for you a fully interactive and visual interface where you can perform the searches for your own website. So,  right now is by  default available at the route '<your_url>/ponywhoosh'. This route  would get you to  this html template:

|Pony|

These form was made thinking in what is more important (query, fields, add wildcards or something, and models). Then if you submit the search, it would show you the results in a parametrized way, deppending on the name of your tables and whether they are searcheables or not. For instance, the example app we provided in here would look like this after you perform some  search:

|Results|

To run this template, you only have to add to your own route the extension /ponywhoosh  and it would redirect you to the personalized view for your own searches. It is possible to change this '/ponywhoosh' route, take a look in the Flask settings section. 

So far is possible to limitate the search to those fields and models where you want to search and even for those that you want to avoid. As well we include check boxes for add_wildcard and something functions. If there are not results to show the table won't be created. 

This is how it looks with the new changes.

|Form| 

Enjoy it! 


.. |Pony| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/doc/_static/searchform.png?raw=true
    :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
.. |Results| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/doc/_static/results.png?raw=true
    :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
.. |Form| image::https://github.com/compiteing/flask-ponywhoosh/blob/master/doc/_static/searchformadvanced.png?raw=true
    :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
