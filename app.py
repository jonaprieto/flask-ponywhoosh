import os
from flask import Flask, jsonify
from pony.orm import *
from pony.orm.serialization import to_json
from flask.ext.script import Manager, Shell
from whoosh.index import *
from whoosh import *
from whoosh.fields import *
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

from entidades import User, Entry, Atributos


@app.route("/llenar")
def llenar():
    with db_session:
        u1 = User(name=u'chuck', edad=13, tipo=u'cliente')
        u2 = User(name=u'arnold', edad=16, tipo=u'proveedor')
        u3 = User(name=u'silvester', edad=17, tipo=u'admin')
        u4 = User(name=u'jonathan', edad=15, tipo=u'cliente')
        u5 = User(name=u'felipe', edad=19, tipo=u'proveedor')
        u6 = User(name=u'harol', edad=16)
        u4= User(name=u'harol',edad=17)
        e1 = Entry(
            title=u'chuck nr. 1 article', content=u'blah blah blah', user=u1)
        e2 = Entry(
            title=u'norris nr. 2 article', content=u'spam spam spam', user=u1)
        e3 = Entry(title=u'arnold blah', content=u'spam is cool', user=u2)
        e4 = Entry(
            title=u'the less dangerous', content=u'chuck is better', user=u3)
        # a1 = Atributos(user=u1, peso=75, deporte=u'tejo')
        # a2 = Atributos(user=u2,  peso=80, deporte=u'lucha de gallinas')
        # a3 = Atributos(user=u3,  peso=65, deporte=u'futbol shaulin')
        # a4 = Atributos(user=u4,  peso=60, deporte=u'caza de marranos')
        # a5 = Atributos(user=u5,  peso=70, deporte=u'lanzamiento de chulo')
        # a6 = Atributos(user=u6,  peso=71, deporte=u'rasking ball')

    return 'base de datos.'


@app.route("/update")
def update1():
    with db_session:
        u = User.get(id=1)
        u.name = "malosito"
        return to_json(u)

#@app.rout ("/buscador")
#def buscar():

#@app.route("/Indice")
#def indice():
   # indice = open_dir('whooshee/user')
    #tabla = Schema(name=TEXT(stored=True), 
     #               edad=NUMERIC(stored=True,
      #              sortable=True))
   # ix = create_in(indice,tabla)
    #writer = ix.writer
   
    #with db_session:
       # for p in select(p for p in User):
           #    writer.add_document(name=p.name, edad=p.edad)
        #writer.commit(optimize=True)

@app.route("/delete/<id>")
def delete(id):
    with db_session:
        u=User.get(id=id)
        u.delete()
        return 'OK'


@app.route("/")
@db_session
def hello():
    with db_session:
        return to_json(User.select())
    return "Nada"

if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
    manager.run()
