import os

from flask import Flask, jsonify
from flask.ext.script import Manager, Shell

from pony.orm import *
from pony.orm.serialization import to_json

from flask_ponywhoosh import Whoosh

#   Create the flask application

app = Flask(__name__)
app.debug = True

wh = Whoosh(app)  # this is our whoosh instance

# It allow us to call the app with:
# $ python app.py runserver
manager = Manager(app)
manager.add_command("shell", Shell(use_bpython=True))

#   Setting the options for PonyWhoosh

app.config['WHOOSHEE_DIR'] = 'whooshes'
app.config['WHOSHEE_MIN_STRING_LEN'] = 1
app.config['WHOOSHEE_WRITER_TIMEOUT'] = 2

# database creation
if not os.path.exists('test.sqlite'):
    f = open('test.sqlite', 'w')
    f.close()

db = Database()

@wh.register_model('name', 'age', sortable=True, stored=True)
class User(db.Entity):
    _table_ = 'User'
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)
    age = Optional(int)
    attrs = Set("Attribute")


@wh.register_model('weight', 'sport', stored=True, sortable=True)
class Attribute(db.Entity):
    _table_ = 'Attribute'
    id = PrimaryKey(int, auto=True)
    user = Optional("User")
    weight = Optional(int)
    sport = Optional(unicode)

db.bind('sqlite', 'test.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

#   /fixtures populate the database

@app.route("/fixtures")
@db_session
def fixtures():
    u1 = User(name=u'chuck', age=u'13')
    u2 = User(name=u'arnold', age=u'16')
    u3 = User(name=u'silvester', age=u'17')
    u4 = User(name=u'jonathan', age=u'15')
    u5 = User(name=u'felipe', age=u'19')
    u6 = User(name=u'harol', age=u'16')
    u7 = User(name=u'harol', age=u'17')

    a1 = Attribute(user=u1, weight=75, sport=u'tejo')
    a2 = Attribute(user=u2, weight=80, sport=u'lucha de gallinas')
    a3 = Attribute(user=u3, weight=65, sport=u'futbol shaulin')
    a4 = Attribute(user=u4, weight=60, sport=u'caza de marranos')
    a5 = Attribute(user=u5, weight=70, sport=u'lanzamiento de chulo')
    a6 = Attribute(user=u6, weight=71, sport=u'rasking ball')

    return '0k', 200


@app.route("/update")
def update():
    with db_session:
        u = User.get(id=1)
        u.name = "evil"
        return to_json(u)


@app.route("/delete/<id>")
@db_session
def delete(id):
    u = User.get(id=id)
    u.delete()
    return 'user_id=%d deleted' % id, 200


@app.route("/")
@db_session
def hello():
    return to_json(User.select())

if __name__ == "__main__":
    manager.run()
