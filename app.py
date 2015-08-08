import os
from flask import Flask, jsonify
from pony.orm import *
from pony.orm.serialization import to_json
from flask.ext.script import Manager, Shell

app = Flask(__name__)
manager = Manager(app)
manager.add_command("shell", Shell(use_bpython=True))

app.debug = True

# app.config['WHOOSHEE_DIR'] = 'whooshes'
# app.config['WHOSHEE_MIN_STRING_LEN'] = 3
# app.config['WHOOSHEE_WRITER_TIMEOUT'] = 2

if not os.path.exists('test.sqlite'):
    f = open('test.sqlite', 'w')
    f.close()

from entidades import db

db.bind('sqlite', 'test.sqlite', create_db=True)

from entidades import User, Entry

@app.route("/llenar")
def llenar():
  with db_session:
      u1 = User(name=u'chuck', tipo='cliente')
      u2 = User(name=u'arnold', tipo = 'proveedor')
      u3 = User(name=u'silvester', tipo='admin')
      u4 = User(name=u'jonathan', tipo='cliente')
      u5 = User(name=u'felipe', tipo='proveedor')
      u6 = User(name=u'harol')
      e1 = Entry(title=u'chuck nr. 1 article', content=u'blah blah blah', user=u1)
      e2 = Entry(title=u'norris nr. 2 article', content=u'spam spam spam', user=u1)
      e3 = Entry(title=u'arnold blah', content=u'spam is cool', user=u2)
      e4 = Entry(title=u'the less dangerous', content=u'chuck is better', user=u3)
  return 'base de datos.'

@app.route("/update")
def update1():
  with db_session:
    u = User.get(id = 1)
    u.name = "malosito"
    return to_json(u)

@app.route("/")
@db_session
def hello():
    with db_session:
        return to_json(User.select())
    return "Nada"

if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
    manager.run()
