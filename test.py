import shutil
import os
import tempfile
from unittest import TestCase

import whoosh
from flask import Flask
from pony.orm import *
from pprint import pprint

from flask_ponywhoosh import Whoosh, search

# from flask_ponywhoosh import *
# from pprint import pprint
# from app import *
# User._wh_.charge_documents()
# User._wh_.counts()
# Attribute._wh_.charge_documents()
# Attribute._wh_.counts()
# pprint(search(User, "har"))
# pprint(search(User, "har", add_wildcards=True))
# pprint(search(User, "har", something = True))
# pprint(full_search(wh, "har"))
# pprint(full_search(wh, "har", something=True))
# pprint(wh.search("har", something=True))
# pprint(search(Attribute, 'marrano'))
# pprint(search(Attribute, 'marrano', add_wildcards=True))
# pprint(search(Attribute, 'marrano', add_wildcards=True, field='name'))
# pprint(search(Attribute, 'tejo', sortedby='weight'))




class BaseTestCases(object):

    class BaseTest(TestCase):

        def __init__(self, *args, **kwargs):
            super(BaseTestCases.BaseTest, self).__init__(*args, **kwargs)
            self.app = Flask(__name__)
            self.app.config['WHOOSHEE_DIR'] = tempfile.mkdtemp()
            self.app.config['TESTING'] = True  
            
        def setUp(self):
            self.db = Database()
            @self.wh.register_model('name', 'age',stored=True,sortable=True)
            class User(self.db.Entity):
                _table_ = 'User'
                id = PrimaryKey(int, auto=True)
                name = Required(unicode)
                age = Optional(int)
                attributes = Set('Attribute')

            @self.wh.register_model('weight','sport',stored= True, sortable=True)
            class Attribute(self.db.Entity):
                _table_='Attribute'
                id = PrimaryKey(int, auto=True)
                name=Optional(unicode)
                user=Optional("User")
                weight=Required(unicode)
                sport=Optional(unicode)     
            
            self.db.bind('sqlite', 'test.sqlite', create_db=True)
            self.db.generate_mapping(create_tables=True)                            
            self.User = User
            self.Attribute = Attribute

        @db_session
        def fixtures(self):   
            self.u1 = self.User(name=u'jonathan', age=u'15')
            self.u2 = self.User(name=u'felipe', age=u'19')
            self.u3 = self.User(name=u'harol', age=u'16')
            self.a1 = self.Attribute(name=u'tejo', user=self.u1, weight=u'75', sport=u'tejo')
            self.a2 = self.Attribute(name=u'gallo', user=self.u2, weight=u'80', sport=u'lucha de gallinas')
            self.a3 = self.Attribute(name=u'ejote', user=self.u3, weight=u'65', sport=u'futbol shaulin')
        
      
        def tearDown(self):
            shutil.rmtree(self.app.config['WHOOSHEE_DIR'], ignore_errors=True)
            self.wh.delete_whoosheers()
            self.db.drop_all_tables(with_all_data=True)
            os.remove('test.sqlite')

         # tests testing model whoosheers should have mw in their name, for custom whoosheers it's cw
         # ideally, there should be a separate class for model whoosheer and custom whoosheer
         # but we also want to test how they coexist
        
        def test_mw_result_in_different_fields(self):
            self.fixtures()

            found = self.User._wh_.search('harol')
            pprint(found)
            self.assertEqual(found['cant_results'], 1)
            self.assertEqual(self.u3.id, found['results'][0]['result'].id)




class TestsWithApp(BaseTestCases.BaseTest):

    def setUp(self):

        self.wh = Whoosh(self.app)

        super(TestsWithApp, self).setUp()

class TestsWithInitApp(BaseTestCases.BaseTest):

    def setUp(self):

        self.wh = Whoosh()
        self.wh.init_app(self.app)

        super(TestsWithInitApp, self).setUp()
