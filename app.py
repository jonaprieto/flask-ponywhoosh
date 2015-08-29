import os

from flask import Flask, jsonify
from flask.ext.script import Manager, Shell

from pony.orm import *
from pony.orm.serialization import to_json

#   Create the flask application

app = Flask(__name__)
app.debug = True

manager = Manager(app)
manager.add_command("shell", Shell(use_bpython=True))

#   Setting the options for PonyWhoosh

app.config['WHOOSHEE_DIR'] = 'whooshes'
app.config['WHOSHEE_MIN_STRING_LEN'] = 1
app.config['WHOOSHEE_WRITER_TIMEOUT'] = 2

if not os.path.exists('test.sqlite'):
    f = open('test.sqlite', 'w')
    f.close()

from entidades import db, User, Atributos
db.bind('sqlite', 'test.sqlite', create_db=True)


#   /fixtures populate the database

@app.route("/fixtures")
@db_session
def fixtures():
    u1 = User(name=u'chuck', edad=u'13', tipo=u'cliente')
    u2 = User(name=u'arnold', edad=u'16', tipo=u'proveedor')
    u3 = User(name=u'silvester', edad=u'17', tipo=u'admin')
    u4 = User(name=u'jonathan', edad=u'15', tipo=u'cliente')
    u5 = User(name=u'felipe', edad=u'19', tipo=u'proveedor')
    u6 = User(name=u'harol', edad=u'16')
    u4 = User(name=u'harol', edad=u'17')

    a1 = Atributos(user=u1, peso=75, deporte=u'tejo')
    a2 = Atributos(user=u2, peso=80, deporte=u'lucha de gallinas')
    a3 = Atributos(user=u3, peso=65, deporte=u'futbol shaulin')
    a4 = Atributos(user=u4, peso=60, deporte=u'caza de marranos')
    a5 = Atributos(user=u5, peso=70, deporte=u'lanzamiento de chulo')
    a6 = Atributos(user=u6, peso=71, deporte=u'rasking ball')

    return '0k', 200


@app.route("/update")
def update1():
    with db_session:
        u = User.get(id=1)
        u.name = "malosito"
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
    db.generate_mapping(create_tables=True)
    manager.run()
