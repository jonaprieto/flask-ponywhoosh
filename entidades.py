from pony.orm import *

db = Database()

class User(db.Entity):
	id = PrimaryKey(int, auto=True)
	name = Required(str)
	entries = Set("Entry")


class Entry(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Optional(str)
    content = Optional(str)
    user = Optional("User")


sql_debug(True)