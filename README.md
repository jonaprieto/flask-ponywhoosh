# Flask-PonyWhoosh
This package integrate the amazing power of `Whoosh` with `Pony ORM` inside  `Flask`.

## Installation

```python

    pip install flask-ponywhoosh
```

## Usage
Import the library where you define your Entities.

```python 
    from flask_ponywhoosh import Whoosh
    wh = Whoosh()
```
And for each entity wrapped it with the decorator `@wh.register_model(*args,**kw)`. like the following example:


```python
@wh.register_model('name','edad',sortable=True,  stored=True)
class User(db.Entity):
    _table_ = 'User'
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)
    tipo = Optional(unicode)
    edad = Optional(unicode)
    entries = Set("Entry")
    atributos = Set("Atributos")
```

As you  appreciate in the previous example, you should declare  as strings the fields where you want whoosh to index (the searcheables), at the same time you might  add several parameters for fields. (sortable, stored, scored, etc.)

### Parameters for Flask Settings

From flask configuration, you could add option for whoosh:

```python
    app.config['WHOOSHEE_DIR'] = 'whooshes'
    app.config['WHOSHEE_MIN_STRING_LEN'] = 3
    app.config['WHOOSHEE_WRITER_TIMEOUT'] = 2
```

### `PonyModel._whoosh_search_(query, **kwargs)`
To execute a search, choose the entity of interest and then, try something like the following code over a view function, or even from the shell.

```python
    >>> from entidades import *
    >>> User._whoosh_search_("felipe")
    {'runtime': 0.002643108367919922, 'results': [User[12], User[5]]}
    >>> from flask_ponywhoosh import search
    >>> search(User,"felipe")
    {'runtime': 0.0016570091247558594, 'results': [User[12], User[5]]}
    >>> search(User,"felipe",sortedby="edad")
    {'runtime': 0.0015339851379394531, 'results': [User[12], User[5]]}
    >>> search(User,"harol",sortedby="edad")
    {'runtime': 0.0038590431213378906, 'results': [User[13], User[6], User
    [14], User[7]]}
    >>>

```
In case that you want the results to be ordered by some specific field, you can write something like, 
```python
    >>> from entidades import *
    >>> from flask_ponywhoosh import search
    >>> search(User,"harol", sortedby="edad")
    {'runtime': 0.0026960372924804688, 'results': [User[20], User[13], User[6], User[21], User[14], Us
    er[7]]}
    >>>

```
All the atributes for the class whoosh.searching.search() are available. You only need to separate by comma and add as many atributes as you need. 

## Usage from Example:

-   `app.py` for running the flask app.
-   `entidades.py` where we defined the entities of database for `PonyORM`.

### Running the App


```bash
    pip install virtualenv
    virtualenv --no-site-packages venv
    source venv/bin/activate
    pip install -r requirements.txt
    python app.py runserver

```

After that, you could visit the following urls.
-   `http://localhost:5000/llenar` to create entries for database, examples.
-   `http://localhost:5000/update` to perform an update in an entity with `id=1`.
-   `http://localhost:5000/` to see the entities from database.


### Using the example

Start a session of a shell.

```bash
    python app.py shell
```

Try something like the following sentences:

```python
    >>> from entidades import User
    >>> from flask_ponywhoosh import search
    >>> search(User, 'harol')
    {'runtime': 0.006242990493774414, 'results': [User[49], User[48], User[35], User[34], User[28], User[
27], User[21], User[20], User[14], User[13]]}
```
