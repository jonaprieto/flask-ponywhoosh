# Flask-PonyWhoosh
This is a package to integrate the amazing power of `Whoosh` with `Pony ORM` inside the `Flask`.


## Running the App
Nowadays, you should download the repository and where you locate in the directory. See inside the `app.py` and `entidades.py` how it works.

```bash
    pip install virtualenv
    virtualenv --no-site-packages venv
    source venv/bin/activate
    python app.py runserver

```

After that, you could visit 
-   `http://localhost:5000/llenar`
-   `http://localhost:5000/update`
-   `http://localhost:5000/` to see the entities from database.

##Future

We are going to structure the package for `pip` with appropriate tests.
Add documentation and example of usages.