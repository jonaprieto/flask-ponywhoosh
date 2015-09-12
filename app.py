import os
from flask import Flask, jsonify
from flask.ext.script import Manager, Shell
from pony.orm import *
from pony.orm.serialization import to_json
from flask_ponywhoosh import Whoosh
from datetime import datetime, timedelta

#   Create the flask application

app = Flask(__name__)
app.debug = True


# It allow us to call the app with:
# $ python app.py runserver
manager = Manager(app)
manager.add_command("shell", Shell(use_bpython=True))

#   Setting the options for PonyWhoosh

app.config['WHOOSHEE_DIR'] = 'whooshes'
app.config['WHOSHEE_MIN_STRING_LEN'] = 1
app.config['WHOOSHEE_WRITER_TIMEOUT'] = 3

wh = Whoosh(app)  # this is our whoosh instance

# database creation
if not os.path.exists('test.sqlite'):
    f = open('test.sqlite', 'w')
    f.close()

db = Database()


@wh.register_model('name', 'age', 'birthday', 'active', sortable=True, stored=True)
class User(db.Entity):
    _table_ = 'User'
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)
    age = Optional(int)
    active=Optional(bool)
    birthday=Optional(datetime)
    attrs = Set("Attribute")


@wh.register_model('weight', 'name', 'sport', 'user', stored=True, sortable=True)
class Attribute(db.Entity):
    _table_ = 'Attribute'
    id = PrimaryKey(int, auto=True)
    name = Optional(unicode)
    user = Optional("User")
    weight = Optional(int)
    sport = Optional(unicode)

db.bind('sqlite', 'test.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

#   /fixtures populate the database


@app.route("/fixtures")
@db_session
def fixtures():
    u1 = User(name=u'chuck',birthday=datetime.utcnow(),active=True, age=13)
    u2 = User(name=u'arnold',birthday=datetime.utcnow(),active=True, age=16)
    u3 = User(name=u'silvester',birthday=datetime.utcnow(),active=True, age=17)
    u4 = User(name=u'jonathan',birthday=datetime.utcnow(),active=True, age=15)
    u5 = User(name=u'felipe',birthday=datetime.utcnow(),active=False, age=19)
    u6 = User(name=u'harol',birthday=datetime.utcnow(),active=False, age=16)
    u7 = User(name=u'harol',birthday=datetime.utcnow(),active=True, age=17)

    a1 = Attribute(name=u'tejo', user=u1, weight=75, sport=u'tejo')
    a2 = Attribute(
        name=u'gallo', user=u2, weight=80, sport=u'lucha de gallinas')
    a3 = Attribute(name=u'ejote', user=u3, weight=65, sport=u'futbol shaulin')
    a4 = Attribute(name=u'ball', user=u4, weight=60, sport=u'caza de marranos')
    a5 = Attribute(
        name=u'marrano', user=u5, weight=70, sport=u'lanzamiento de chulo')
    a6 = Attribute(name=u'lanza', user=u6, weight=71, sport=u'rasking ball')

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
