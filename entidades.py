from pony.orm import *
from flask_ponywhoosh import Whoosh
import sys
from types import MethodType

wh = Whoosh(debug=True)
db = Database()

@wh.register_model('name',stored=True)
class User(db.Entity):
    _table_ = 'User'
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)
    tipo = Optional(unicode)
    entries = Set("Entry")


class Entry(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Optional(unicode)
    content = Optional(unicode)
    user = Optional("User")


# sql_debug(True)
