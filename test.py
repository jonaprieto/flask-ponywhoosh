import shutil
import tempfile
from unittest import TestCase

import whoosh
from flask import Flask
from pony import *

from flask_ponywhoosh import Whoosh, search

# from flask_ponywhoosh import *
# from pprint import pprint
# from app import *
# User._wh_.charge_documents()
# User._wh_.counts()
# Attribute._wh_.charge_documents()
# Attribute._wh_.counts()
# search(User, "har")
# search(User, "har", add_wildcards=True)
# search(User, "har", something = True)
# full_search(wh, "har")
# full_search(wh, "har", something=True)
# search(Attribute, 'marrano')
# search(Attribute, 'marrano', add_wildcards=True)
# search(Attribute, 'marrano', add_wildcards=True, field='name')

class BaseTestCases(object):

    class BaseTest(TestCase):

        def __init__(self, *args, **kwargs):
            super(BaseTestCases.BaseTest, self).__init__(*args, **kwargs)
            self.app = Flask(__name__)

            self.app.config['WHOOSHEE_DIR'] = tempfile.mkdtemp()
            self.app.config['TESTING'] = True            
            self.manager = Manager(app)
            self.app.debug = True
            self.db = Database()
            self.db.bind('sqlite', ':memory:', create_db=True)
            self.wh = Whoosh(debug=True)

        def setUp(self):
            pass
        #     @self.wh.register_model('name', 'edad',stored=True)
        #     class User(self.db.Entity):
        #         _table_ = 'User'
        #         id = PrimaryKey(int, auto=True)
        #         name = Required(unicode)
        #         tipo = Optional(unicode)
        #         edad = Optional(int)
        #         entries = Set("Entry")
        #         atributos = Set("Atributos")

        #     # separate index for just Atributos
        #     @self.wh.register_model('edad', 'peso',stored=True)
        #     class Atributos(self.db.Model):
        #         _table_='Atributos'
        #         id = Primarykey(int,auto=True)
        #         deporte = Optional(unicode )
        #         peso = Optional(int)
        #         user = Optional("User")
               
            

        #         models = [Atributos, User]

        #         @classmethod
        #         def update_user(cls, writer, user):
        #             pass # TODO: update all users entries

        #         @classmethod
        #         def update_Atributos(cls, writer, entry):
        #             writer.update_document(entry_id=Atributos.id,
        #                                    user_id=entry.user.id,
        #                                    username=entry.user.name,
        #                                    title=entry.title,
        #                                    content=entry.content)

        #         @classmethod
        #         def insert_user(cls, writer, user):
        #             # nothing, user doesn't have entries yet
        #             pass

        #         @classmethod
        #         def insert_entry(cls, writer, entry):
        #             writer.add_document(entry_id=entry.id,
        #                                 user_id=entry.user.id,
        #                                 name=entry.user.name,
        #                                 edad=entry.title,
        #                                 content=entry.content)

        #     self.User = User
        #     self.Entry = Entry
        #     self.EntryUserWhoosheer = EntryUserWhoosheer

        #     self.db.create_all()

        #     self.u1 = User(name=u'chuck')
        #     self.u2 = User(name=u'arnold')
        #     self.u3 = User(name=u'silvester')

        #     self.e1 = Entry(title=u'chuck nr. 1 article', content=u'blah blah blah', user=self.u1)
        #     self.e2 = Entry(title=u'norris nr. 2 article', content=u'spam spam spam', user=self.u1)
        #     self.e3 = Entry(title=u'arnold blah', content=u'spam is cool', user=self.u2)
        #     self.e4 = Entry(title=u'the less dangerous', content=u'chuck is better', user=self.u3)

        #     self.all_inst = [self.u1, self.u2, self.u3, self.e1, self.e2, self.e3, self.e4]

        # def tearDown(self):
        #     shutil.rmtree(self.app.config['WHOOSHEE_DIR'], ignore_errors=True)
        #     Whooshee.whoosheers = []
        #     self.db.drop_all()

        # # tests testing model whoosheers should have mw in their name, for custom whoosheers it's cw
        # # ideally, there should be a separate class for model whoosheer and custom whoosheer
        # # but we also want to test how they coexist

        # def test_mw_result_in_different_fields(self):
        #     self.db.session.add_all(self.all_inst)
        #     self.db.session.commit()

        #     found = self.Entry.query.whooshee_search('chuck').all()
        #     self.assertEqual(len(found), 2)
        #     # there is no assertIn in Python 2.6
        #     self.assertTrue(self.e1 in found)
        #     self.assertTrue(self.e4 in found)

        # def test_cw_result_in_different_tables(self):
        #     self.db.session.add_all(self.all_inst)
        #     self.db.session.commit()

        #     found = self.Entry.query.join(self.User).whooshee_search('chuck').all()
        #     self.assertEqual(len(found), 3)
        #     self.assertTrue(self.e1 in found)
        #     self.assertTrue(self.e2 in found)
        #     self.assertTrue(self.e4 in found)

        # def test_more_items(self):
        #     expected_count = 0
        #     # couldn't test for large set due to some bugs either in sqlite or whoosh or SA
        #     # got: OperationalError: (OperationalError) too many SQL variables u'SELECT entry.id
        #     #  ... FROM entry \nWHERE entry.id IN (?, ?, .... when whooshee_search is invoked
        #     for batch_size in [2, 5, 7, 20, 50, 300, 500]:  # , 1000]:
        #         expected_count += batch_size
        #         self.entry_list = [
        #             self.Entry(title=u'foobar_{0}_{1}'.format(expected_count, x),
        #                        content=u'xxxx', user=self.u1)
        #             for x in range(batch_size)
        #         ]

        #         self.db.session.add_all(self.entry_list)
        #         self.db.session.commit()

        #         found = self.Entry.query.whooshee_search('foobar').all()
        #         assert len(found) == expected_count

        # # TODO: more :)

class TestsWithApp(BaseTestCases.BaseTest):

    def setUp(self):

        # self.wh = Whooshee(self.app)

        super(TestsWithApp, self).setUp()

# class TestsWithInitApp(BaseTestCases.BaseTest):

#     def setUp(self):

#         self.wh = Whooshee()
#         self.wh.init_app(self.app)

#         super(TestsWithInitApp, self).setUp()
