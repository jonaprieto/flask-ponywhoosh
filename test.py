'''

  flask-ponywhoosh test module
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Perform full-text searches over your database with Pony ORM and PonyWhoosh,
  for flask applications.

  :copyright: (c) 2015-2018 by Jonathan Prieto-Cubides & Felipe Rodriguez.
  :license: MIT (see LICENSE.md)

'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tempfile

from flask            import Flask
from flask_ponywhoosh import PonyWhoosh
from flask_ponywhoosh import search, full_search

from pony.orm         import *
from pprint           import pprint
from unittest         import TestCase


class BaseTestCases(object):

    class BaseTest(TestCase):

        def __init__(self, *args, **kwargs):
            super(BaseTestCases.BaseTest, self).__init__(*args, **kwargs)
            self.app = Flask(__name__)
            self.app.config['PONYWHOOSH_INDEXES_PATH'] = tempfile.mkdtemp()
            self.app.config['DEBUG'] = True

        def setUp(self):
            self.db = Database()

            @self.pw.register_model('name', 'age', stored=True, sortable=True)
            class User(self.db.Entity):
                id = PrimaryKey(int, auto=True)
                name = Required(unicode)
                age = Optional(int)
                attributes = Set('Attribute')

            @self.pw.register_model('weight', 'sport', 'name', stored=True, sortable=True)
            class Attribute(self.db.Entity):
                id = PrimaryKey(int, auto=True)
                name = Optional(unicode)
                user = Optional("User")
                weight = Required(unicode)
                sport = Optional(unicode)

            self.db.bind('sqlite', ':memory:', create_db=True)
            self.db.generate_mapping(create_tables=True)
            self.User = User
            self.Attribute = Attribute

        @db_session
        def fixtures(self):
            self.u1 = self.User(name=u'jonathan', age=u'15')
            self.u2 = self.User(name=u'felipe', age=u'19')
            self.u3 = self.User(name=u'harol', age=u'16')
            self.u4 = self.User(name=u'felun', age=u'16')
            self.a1 = self.Attribute(name=u'felun', user=self.u1, weight=u'80', sport=u'tejo')
            self.a2 = self.Attribute(name=u'galun', user=self.u2, weight=u'75', sport=u'lucha de felinas')
            self.a3 = self.Attribute(name=u'ejote', user=self.u3, weight=u'65', sport=u'futbol shaulin')

        def tearDown(self):
            shutil.rmtree(self.app.config['PONYWHOOSH_INDEXES_PATH'], ignore_errors=True)
            self.pw.delete_indexes()
            self.db.drop_all_tables(with_all_data=True)
            # os.remove('test.sqlite')

         # tests testing model whoosheers should have mw in their name, for custom whoosheers it's cw
         # ideally, there should be a separate class for model whoosheer and custom whoosheer
         # but we also want to test how they coexist

        def test_search(self):
            self.fixtures()
            found = self.User._pw_index_.search('harol', include_entity=True)
            self.assertEqual(found['cant_results'], 1)
            self.assertEqual(self.u3.id, found['results'][0]['entity']['id'])

        def test_search_something(self):
            self.fixtures()
            found = self.User._pw_index_.search('har', something=True, include_entity=True)
            self.assertEqual(found['cant_results'], 1)

        def test_full_search_without_wildcards(self):
            self.fixtures()

            found = full_search(self.pw, "fel")
            self.assertEqual(found['cant_results'], 0)

        def test_full_search_with_wildcards(self):
            self.fixtures()

            found = full_search(self.pw, "fel", add_wildcards=True, include_entity=True)
            self.assertEqual(found['cant_results'], 4)

        def test_fields(self):
            self.fixtures()
            results = full_search(self.pw, "felun", include_entity=True, fields=["name"])
            self.assertEqual(results['cant_results'], 2)

        def test_models(self):
            self.fixtures()
            results = full_search(self.pw, "felun", include_entity=True, models=['User'])
            self.assertEqual(results['cant_results'], 1)

        def test_except_field(self):
            self.fixtures()
            results = full_search(self.pw, "felun", except_fields=["name"])
            self.assertEqual(results['cant_results'], 0)

class TestsWithApp(BaseTestCases.BaseTest):

    def setUp(self):
        self.pw = PonyWhoosh(self.app)
        super(TestsWithApp, self).setUp()


class TestsWithInitApp(BaseTestCases.BaseTest):

    def setUp(self):
        self.pw = PonyWhoosh()
        self.pw.init_app(self.app)

        super(TestsWithInitApp, self).setUp()
