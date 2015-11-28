====================
Bonus:/ponywhoosh ! 
====================

To run this template, you only have to add to your own route the extension /ponywhoosh  and it would redirect you to the personalized view for your own searches. It is possible to change this '/ponywhoosh' route, take a look in the Flask settings section. 

So far is possible to limitate the search to those fields and models where you want to search and even for those that you want to avoid. As well we include check boxes for add_wildcard and something functions. If there are not results to show the table won't be created.

Search Form
***********
|Pony|

We  aknowledged  that  we could do better rendering  the results, for this reason we thought that it would be nice and useful to get ready for you a fully interactive and visual interface where you can perform the searches for your own website. So  right now is by  default available at the route '<your_url>/ponywhoosh'. 



Advanced search form
********************

|Form| 

In this advanced form you can filter your search using the options available from whoosh (query, fields, add wildcards or something, and models). 

	The  fields text input is a StringField where you can type, separated by commas, all the fields where you want to search. If a field is not available the search would be performed as a full_search one. 

	Add_wildcars: Is a checkbox that indicates that you will  perform inexact searching.

	Something: A checkbox that let you perform a search using exact terms, but if is not able to find anything it would perform a search using add_wildcards. 

	Models: The models input is a StringField where you can type, separated by commas, all the models where you want to search.

It is available in the top of the view, like this: 

|TopForm

Results
*******


|Results|

The result template renderizes all the results in the following way:
	In the upper part you will see tabs containing all the Indexes where Ponywhoos found something. 

	There are two options to view the resuls. Like a card or like a table. In the first one you would see 3 cards by line, showing the main results attributes. When you are registering the models, they would be the 3 first fields you register. 
 

This is how it looks with the new changes.

Enjoy it! 


.. |Pony| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/docs/_static/searchform.png?raw=true
    :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
.. |Results| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/docs/_static/results.png?raw=true
    :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
.. |Form| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/docs/_static/searchformadvanced.png?raw=true
    :target: https://travis-ci.org/piperod/Flask-PonyWhoosh
