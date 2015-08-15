# Flask-PonyWhoosh
This is a package to integrate the amazing power of `Whoosh` with `Pony ORM` inside the `Flask`.

## Installation

```python

    pip install flask-ponywhoosh
```

## Usage
Let look at example: `app.py` for running the flask app, and `entidades.py` where we defined the entities of database for `PonyORM`.

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

Inside it, code the following:

```python
    >>> from entidades import User
    >>> from flask_ponywhoosh import search
    >>> search(User, 'jona')
    
```
