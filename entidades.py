from pony.orm import *
from flask_ponywhoosh import Whoosh , search
import sys
from types import MethodType

wh = Whoosh(debug=True)
db = Database()
wh.search_string_min_len=1
@wh.register_model('name','edad',sortable=True,  stored=True)
class User(db.Entity):
    _table_ = 'User'
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)
    tipo = Optional(unicode)
    edad = Optional(int)
    entries = Set("Entry")
    atributos = Set("Atributos")

@wh.register_model('peso','deporte', stored = True, sortable=True)
class Atributos(db.Entity):
    _table_ = 'Atributos'
    id = PrimaryKey(int, auto=True)
    user = Optional("User")
    peso = Optional(int)
    deporte = Optional(unicode)


class Entry(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Optional(unicode)
    content = Optional(unicode)
    user = Optional("User")


# sql_debug(True)
