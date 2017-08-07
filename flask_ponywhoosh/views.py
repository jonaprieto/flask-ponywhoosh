'''

  flask_ponywhoosh.views module
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Perform full-text searches over your database with Pony ORM and PonyWhoosh,
  for flask applications.

  :copyright: (c) 2015-2017 by Jonathan Prieto-Cubides & Felipe Rodriguez.
  :license: MIT (see LICENSE.md)

'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

from pprint      import pprint
from flask       import render_template
from flask.views import View
from .form       import SearchForm


class IndexView(View):
  """This is all the setting for the template index.html in the templates folder.
      methods (list): POST and GET
  """

  methods = ['POST', 'GET']

  def __init__(self, pw, action_url_form):
    self._pw              = pw
    self.debug            = self._pw.debug
    self.action_url_form  = action_url_form

  def dispatch_request(self):
    """ This form is plugeable. That means that all what you need to do is
    to install the package and run the url :: /ponywhoosh/
    (You may change it in the config) and get the results.

    Returns:
      Results: The results are sent to the template using bootstrap.
      They are renderized using whether a grid or a table, depending on what
      models did you register.
      By default the first field registered is considered the one that will
      be contained in the tittle of each searh result.
    """

    ctx           = {'form' : SearchForm()}
    except_field  = None
    query, fields = None, None
    wildcards     = True
    form          = SearchForm()

    if self.debug:
      print('form:')
      pprint(form.data)

    if form.validate_on_submit():

      add_wildcards = form.add_wildcards.data
      except_fields = re.split('\W+', form.except_field.data, flags=re.UNICODE)
      fields    = re.split('\W+', form.fields.data, flags=re.UNICODE)
      models    = re.split('\W+', form.models.data, flags=re.UNICODE)
      query     = form.query.data
      something = form.something.data

      results = self._pw.search(
          query
        , add_wildcards=add_wildcards
        , something=something
        , include_entity=True
        , fields=fields
        , models=models
        , except_fields=except_fields
        , use_dict=False
      )

      if self.debug:
        print('form = ')
        pprint({
            'query': query
          , 'add_wildcards': add_wildcards
          , 'something': something
          , 'include_entity': True
          , 'fields': fields
          , 'models': models
          , 'except_fields': except_fields
        })

        print("results = ")
        pprint(results)

      return render_template(
          'ponywhoosh/results.html'
        , entidades=list(self._pw._entities.keys())
        , action_url_form=self.action_url_form
        , form=form
        , results=results
        , n=results['cant_results']
        , labels=results['results'].keys()
      )

    return render_template(
      'ponywhoosh/index.html'
      , form=form
      , action_url_form=self.action_url_form
      , query=query
    )
