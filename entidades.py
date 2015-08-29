from pony.orm import *
from flask_ponywhoosh import Whoosh, search
import sys
from types import MethodType

db = Database()


wh = Whoosh(debug=True)

@wh.register_model('name', 'edad', sortable=True,  stored=True)
class User(db.Entity):
    _table_ = 'User'
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)
    tipo = Optional(unicode)
    edad = Optional(int)
    entries = Set("Entry")
    atributos = Set("Atributos")


@wh.register_model('peso', 'deporte', stored=True, sortable=True)
class Atributos(db.Entity):
    _table_ = 'Atributos'
    id = PrimaryKey(int, auto=True)
    user = Optional("User")
    peso = Optional(int)
    deporte = Optional(unicode)
