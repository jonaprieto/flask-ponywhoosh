import os
from pprint import pprint
import shutil
import tempfile
from unittest import TestCase

from flask import Flask
from flask_ponywhoosh import Whoosh, search, full_search
from pony.orm import *
import whoosh


class BaseTestCases(object):

    class BaseTest(TestCase):

        def __init__(self, *args, **kwargs):
            super(BaseTestCases.BaseTest, self).__init__(*args, **kwargs)
            self.app = Flask(__name__)
            self.app.config['WHOOSHEE_DIR'] = tempfile.mkdtemp()
            self.app.config['TESTING'] = True

        def setUp(self):
            self.db = Database()

            @self.wh.register_model('name', 'age', stored=True, sortable=True)
            class User(self.db.Entity):
                _table_ = 'User'
                id = PrimaryKey(int, auto=True)
                name = Required(unicode)
                age = Optional(int)
                attributes = Set('Attribute')

            @self.wh.register_model('weight', 'sport', 'name', stored=True, sortable=True)
            class Attribute(self.db.Entity):
                _table_ = 'Attribute'
                id = PrimaryKey(int, auto=True)
                name = Optional(unicode)
                user = Optional("User")
                weight = Required(unicode)
                sport = Optional(unicode)

            self.db.bind('sqlite', 'test.sqlite', create_db=True)
            self.db.generate_mapping(create_tables=True)
            self.User = User
            self.Attribute = Attribute

        @db_session
        def fixtures(self):
            self.u1 = self.User(name=u'jonathan', age=u'15')
            self.u2 = self.User(name=u'felipe', age=u'19')
            self.u3 = self.User(name=u'harol', age=u'16')
            self.a1 = self.Attribute(
                name=u'felun', user=self.u1, weight=u'80', sport=u'tejo')
            self.a2 = self.Attribute(
                name=u'galun', user=self.u2, weight=u'75', sport=u'lucha de felinas')
            self.a3 = self.Attribute(
                name=u'ejote', user=self.u3, weight=u'65', sport=u'futbol shaulin')

        def tearDown(self):
            shutil.rmtree(self.app.config['WHOOSHEE_DIR'], ignore_errors=True)
            self.wh.delete_whoosheers()
            self.db.drop_all_tables(with_all_data=True)
            os.remove('test.sqlite')

         # tests testing model whoosheers should have mw in their name, for custom whoosheers it's cw
         # ideally, there should be a separate class for model whoosheer and custom whoosheer
         # but we also want to test how they coexist

        def test_search(self):
            self.fixtures()
            found = self.User._wh_.search('harol', include_entity=True)
            self.assertEqual(found['cant_results'], 1)
            self.assertEqual(self.u3.id, found['results'][0]['entity']['id'])

        def test_search_something(self):
            self.fixtures()
            found = self.User._wh_.search(
                'har', something=True, include_entity=True)
            self.assertEqual(found['cant_results'], 1)

        def test_search_sortedby(self):
            self.fixtures()
            found = self.Attribute._wh_.search(
                'lun', add_wildcards=True, sortedby="weight", include_entity=True)
            self.assertEqual(self.a2.id, found['results'][0]['entity']['id'])
            self.assertEqual(self.a1.id, found['results'][1]['entity']['id'])

        def test_full_search_without_wildcards(self):
            self.fixtures()

            found = full_search(self.wh, "fel")
            self.assertEqual(found['cant_results'], 0)

        def test_full_search_with_wildcards(self):
            self.fixtures()

            found = full_search(
                self.wh, "fel", add_wildcards=True, include_entity=True)
            self.assertEqual(found['cant_results'], 3)

class TestsWithApp(BaseTestCases.BaseTest):

    def setUp(self):

        self.wh = Whoosh(self.app)

        super(TestsWithApp, self).setUp()


class TestsWithInitApp(BaseTestCases.BaseTest):

    def setUp(self):

        self.wh = Whoosh()
        self.wh.init_app(self.app)

        super(TestsWithInitApp, self).setUp()
