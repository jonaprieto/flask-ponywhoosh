'''

  flask_ponywhoosh.form module
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Perform full-text searches over your database with Pony ORM and PonyWhoosh,
  for flask applications.

  :copyright: (c) 2015-2017 by Jonathan Prieto-Cubides & Felipe Rodriguez.
  :license: MIT (see LICENSE.md)

'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask_wtf          import Form
from wtforms            import StringField, SubmitField
from wtforms            import BooleanField, SelectField
from wtforms.validators import Required


class SearchForm(Form):
  """This is the searching form that we will be use to make our search
  engine website.

  Attributes:
      except_field (StringField): Fields you do not want to include in the search results.
      fields (StringField): Fields, separated by comma,  where you want to search.
      models (StringField): Models, separated by comma, where you want to search.
      query (StringField): What you want to search.
      something (BooleanField): Option to literal search first, but in case there are no results available, it performs a search with wild_cards.
      submit (SubmitField): Button to submit the form.
      wildcards (BooleanField): Checkbox
  """

  add_wildcards   = BooleanField('Add Wildcards', default=True)
  except_field    = StringField('Except in Fields')
  fields          = StringField('Fields')
  models          = StringField('Models')
  query           = StringField('What are you looking for?')
  something       = BooleanField('Something')
  submit          = SubmitField('Submit')
