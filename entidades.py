from pony.orm import *
from flask_whooshpony import Whoosh
import sys
from types import MethodType

wh = Whoosh(debug=True)
db = Database()

@wh.register_model('name',stored=True)
class User(db.Entity):
    _table_ = 'User'
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    tipo = Optional(str)
    entries = Set("Entry")

class Entry(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Optional(str)
    content = Optional(str)
    user = Optional("User")


# sql_debug(True)
