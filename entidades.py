from pony.orm import *
from flask_ponywhoosh import Whoosh
import sys
from types import MethodType

wh = Whoosh(debug=True)
db = Database()


@wh.register_model('name','edad',sortable=True,  stored=True)
class User(db.Entity):
    _table_ = 'User'
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)
    tipo = Optional(unicode)
    edad = Optional(unicode)
    entries = Set("Entry")
    atributos = Set("Atributos")


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
