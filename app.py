import os
from flask import Flask, jsonify
from pony.orm import *
from pony.orm.serialization import to_json

app = Flask(__name__)
app.debug = True

from flask_whooshpony import Whoosh

wh = Whoosh(app)


from entidades import db

if not os.path.exists('test.sqlite'):
    f = open('test.sqlite', 'w')
    f.close()

db.bind('sqlite', 'test.sqlite', create_db=True)

from entidades import User, Entry
@app.route("/llenar")
def llenar():
  with db_session:
      u1 = User(name=u'chuck')
      u2 = User(name=u'arnold')
      u3 = User(name=u'silvester')
      e1 = Entry(title=u'chuck nr. 1 article', content=u'blah blah blah', user=u1)
      e2 = Entry(title=u'norris nr. 2 article', content=u'spam spam spam', user=u1)
      e3 = Entry(title=u'arnold blah', content=u'spam is cool', user=u2)
      e4 = Entry(title=u'the less dangerous', content=u'chuck is better', user=u3)
  return 'base de datos.'


@app.route("/")
@db_session
def hello():
    with db_session:
        return to_json(User.select())
    return "Nada"

if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
    app.run()
