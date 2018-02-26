'''

  flask-ponywhoosh example
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Perform full-text searches over your database with Pony ORM and PonyWhoosh,
  for flask applications.

  :copyright: (c) 2015-2018 by Jonathan Prieto-Cubides & Felipe Rodriguez.
  :license: MIT (see LICENSE.md)

'''

import os

from datetime               import datetime, timedelta, date
from flask                  import Flask, jsonify, render_template
from flask_bootstrap        import Bootstrap
from flask_ponywhoosh       import PonyWhoosh
from flask_script           import Manager, Shell
from pony.orm               import *
from pony.orm.serialization import to_json


app         = Flask(__name__)
app.debug   = True

manager = Manager(app)
manager.add_command("shell", Shell(use_bpython=True))

# -----------------------------------------------------------------------------
#
# Options for PonyWhoosh package
#
# -----------------------------------------------------------------------------

app.config['PONYWHOOSH_DEBUG']              = True
app.config['PONYWHOOSH_DIR']                = 'whooshes'
app.config['PONYWHOOSH_MIN_STRING_LEN']     = 1
app.config['PONYWHOOSH_URL_ROUTE']          = '/'
app.config['PONYWHOOSH_WRITER_TIMEOUT']     = 3
app.config['SECRET_KEY']                    = 'hard to guess string'

# -----------------------------------------------------------------------------

bootstrap   = Bootstrap(app)
db          = Database()
pw          = PonyWhoosh(app)


@pw.register_model('number', 'name')
class Department(db.Entity):
  number  = PrimaryKey(int, auto=True)
  name    = Required(str, unique=True)
  groups  = Set("Group")
  courses = Set("Course")


@pw.register_model('number', 'major')
class Group(db.Entity):
  number    = PrimaryKey(int)
  major     = Required(str)
  dept      = Required("Department")
  students  = Set("Student")


@pw.register_model('name', 'semester', 'lect_hours', 'lab_hours', 'credits')
class Course(db.Entity):
  name        = Required(str)
  semester    = Required(int)
  lect_hours  = Required(int)
  lab_hours   = Required(int)
  credits     = Required(int)
  dept        = Required(Department)
  students    = Set("Student")
  PrimaryKey(name, semester)


@pw.register_model('name', 'tel', 'gpa')
class Student(db.Entity):
  id        = PrimaryKey(int, auto=True)
  name      = Required(str)
  dob       = Required(date)
  tel       = Optional(str)
  picture   = Optional(buffer, lazy=True)
  gpa       = Required(float, default=0)
  group     = Required(Group)
  courses   = Set(Course)

db.bind('sqlite', 'example.sqlite', create_db=True)
#db.bind('mysql', host="localhost", user="pony", passwd="pony", db="university1")
#db.bind('postgres', user='pony', password='pony', host='localhost'
#  , database='university1')
#db.bind('oracle', 'university1/pony@localhost')


db.generate_mapping(create_tables=True)


@db_session
def populate_database():
  if select(s for s in Student).count() > 0: return
  d1 = Department(name="Department of Computer Science")
  d2 = Department(name="Department of Mathematical Sciences")
  d3 = Department(name="Department of Applied Physics")

  c1 = Course(
      name="Web Design"
    , semester=1
    , dept=d1
    , lect_hours=30
    , lab_hours=30
    , credits=3
    )
  c2 = Course(
      name="Data Structures and Algorithms"
    , semester=3
    , dept=d1
    , lect_hours=40
    , lab_hours=20
    , credits=4
    )
  c3 = Course(
      name="Linear Algebra"
    , semester=1
    , dept=d2
    , lect_hours=30
    , lab_hours=30
    , credits=4
    )
  c4 = Course(
      name="Statistical Methods"
    , semester=2
    , dept=d2
    , lect_hours=50
    , lab_hours=25
    , credits=5
    )
  c5 = Course(
      name="Thermodynamics"
    , semester=2
    , dept=d3
    , lect_hours=25
    , lab_hours=40
    , credits=4
    )
  c6 = Course(
      name="Quantum Mechanics"
    , semester=3
    , dept=d3
    , lect_hours=40
    , lab_hours=30
    , credits=5
    )
  g101 = Group(
      number=101
    , major='B.E. in Computer Engineering'
    , dept=d1
    )
  g102 = Group(
      number=102
    , major='B.S./M.S. in Computer Science'
    , dept=d1
    )
  g103 = Group(
      number=103
    , major='B.S. in Applied Mathematics and Statistics'
    , dept=d2
    )
  g104 = Group(
      number=104
    , major='B.S./M.S. in Pure Mathematics'
    , dept=d2
    )
  g105 = Group(
      number=105
    , major='B.E in Electronics'
    , dept=d3
    )
  g106 = Group(
      number=106
    , major='B.S./M.S. in Nuclear Engineering'
    , dept=d3
    )
  s1 = Student(
      name='John Smith'
    , dob=date(1991, 3, 20)
    , tel='123-456'
    , gpa=3
    , group=g101
    , courses=[c1, c2, c4, c6]
    )
  s2 = Student(
      name='Matthew Reed'
    , dob=date(1990, 11, 26)
    , gpa=3.5
    , group=g101
    , courses=[c1, c3, c4, c5]
    )
  s3 = Student(
      name='Chuan Qin'
    , dob=date(1989, 2, 5)
    , gpa=4
    , group=g101
    , courses=[c3, c5, c6]
    )

  s4 = Student(
      name='Rebecca Lawson'
    , dob=date(1990, 4, 18)
    , tel='234-567'
    , gpa=3.3
    , group=g102
    , courses=[c1, c4, c5, c6]
    )

  s5 = Student(
      name='Maria Ionescu'
    , dob=date(1991, 4, 23)
    , gpa=3.9
    , group=g102
    , courses=[c1, c2, c4, c6]
    )
  s6 = Student(
      name='Oliver Blakey'
    , dob=date(1990, 9, 8)
    , gpa=3.1
    , group=g102
    , courses=[c1, c2, c5]
    )
  s7 = Student(
      name='Jing Xia'
    , dob=date(1988, 12, 30)
    , gpa=3.2
    , group=g102
    , courses=[c1, c3, c5, c6]
    )
  commit()

@app.route("/database")
@db_session
def index():
  return to_json(Student.select())

if __name__ == "__main__":
  populate_database()
  manager.run()
