'''

  flask_ponywhoosh module
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Perform full-text searches over your database with Pony ORM and PonyWhoosh,
  for flask applications.

  :copyright: (c) 2015-2017 by Jonathan Prieto-Cubides & Felipe Rodriguez.
  :license: MIT (see LICENSE.md)

'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import jinja2
import os

from ponywhoosh  import PonyWhoosh as MyPonyWhoosh
from ponywhoosh  import search, full_search, delete_field
from .views      import IndexView


__all__     = ['PonyWhoosh', 'search', 'full_search', 'delete_field']
__author__  = "Jonathan Prieto-Cubides & Felipe Rodriguez"
basedir     = os.path.abspath(os.path.dirname(__file__))

class PonyWhoosh(MyPonyWhoosh):

  debug           = False
  indexes_path    = 'ponywhoosh_indexes'
  writer_timeout  = 2
  url_route       = '/search/'
  template_path   = os.path.join(basedir, 'templates')
  search_string_min_len = 2


  def __init__(self, app=None):
    super(PonyWhoosh, self).__init__()

    if app is not None:
      self.init_app(app)

    if not os.path.exists(self.indexes_path):
      os.makedirs(self.indexes_path)

  def init_app(self, app):
    """Initializes the App.

    Args:
        app (TYPE): Description

    Returns:
        TYPE: Description
    """

    config = app.config.copy()
    self.debug        = config.get('PONYWHOOSH_DEBUG', self.debug)
    self.indexes_path = config.get('PONYWHOOSH_INDEXES_PATH',  self.indexes_path)
    self.search_string_min_len = config.get('PONYWHOOSH_MIN_STRING_LEN', self.search_string_min_len)
    self.writer_timeout = config.get('PONYWHOOSH_WRITER_TIMEOUT', self.writer_timeout)
    self.url_route      = config.get('PONYWHOOSH_URL_ROUTE', self.url_route)
    self.template_path  = config.get('PONYWHOOSH_TEMPLATE_PATH', self.template_path)

    if self.debug:
      print('PONYWHOOSH_DEBUG -> ', self.debug)
      print('PONYWHOOSH_INDEXES_PATH  -> ', self.indexes_path)
      print('PONYWHOOSH_MIN_STRING_LEN  -> ', self.search_string_min_len)
      print('PONYWHOOSH_TEMPLATE_PATH -> ', self.template_path)
      print('PONYWHOOSH_URL_ROUTE -> ',  self.url_route)
      print('PONYWHOOSH_WRITER_TIMEOUT -> ', self.writer_timeout)

    loader = jinja2.ChoiceLoader([
        app.jinja_loader
      , jinja2.FileSystemLoader(self.template_path)
    ])

    # indexView = IndexView()

    app.jinja_loader = loader
    app.add_url_rule(
        self.url_route
      , view_func=IndexView.as_view(self.url_route
        , pw=self
        , action_url_form=self.url_route
        )
    )