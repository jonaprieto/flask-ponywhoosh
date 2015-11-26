#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: d555
"""

    PonyWhoosh Class
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2015-2016 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
    :license: BSD (see LICENSE.md)

"""

from collections import defaultdict
import os
import re
import sys

import jinja2
from pony import orm
from ponywhooshindex import PonyWhooshIndex
from views import IndexView
from whoosh import fields as whoosh_module_fields
from whoosh import index as whoosh_module_index
from whoosh import qparser
import whoosh

basedir = os.path.abspath(os.path.dirname(__file__))


class PonyWhoosh(object):

    """A top level class that allows to register indexes.

    Attributes:
        * DEBUG (bool): Description
        * indexes_path (str): this is the name where the folder of the indexes are going to be stored.
        * route (TYPE): This config let you set the route for the url to run the html template.
        * search_string_min_len (int): This item let you config the minimun string value possible to perform search.
        * template_path (TYPE): Is the path where the folder of templates will be store.
        * writer_timeout (int): Is the time when the writer should stop the searching.
    """

    indexes_path = 'ponywhoosh_indexes'
    writer_timeout = 2
    search_string_min_len = 2
    debug = False
    url_route = '/ponywhoosh/'
    template_path = os.path.join(basedir, 'templates')

    _indexes = {}
    _entities = {}

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

        if not os.path.exists(self.indexes_path):
            os.makedirs(self.indexes_path)

    def init_app(self, app):
        """Initializes the App.

        Args:
            app (TYPE): Description

        Returns:
            TYPE: Description
        """

        config = app.config.copy()

        self.debug = config.get('PONYWHOOSH_DEBUG', self.debug)
        self.indexes_path = config.get('PONYWHOOSH_INDEXES_PATH',  self.indexes_path)
        self.search_string_min_len = config.get('PONYWHOOSH_MIN_STRING_LEN', self.search_string_min_len)
        self.writer_timeout = config.get('PONYWHOOSH_WRITER_TIMEOUT', self.writer_timeout)
        self.url_route = config.get('PONYWHOOSH_URL_ROUTE', self.url_route)
        self.template_path = config.get('PONYWHOOSH_TEMPLATE_PATH', self.template_path)

        if self.debug:
            print 'PONYWHOOSH_DEBUG -> ', self.debug
            print 'PONYWHOOSH_INDEXES_PATH  -> ', self.indexes_path
            print 'PONYWHOOSH_MIN_STRING_LEN  -> ', self.search_string_min_len
            print 'PONYWHOOSH_WRITER_TIMEOUT -> ', self.writer_timeout
            print 'PONYWHOOSH_TEMPLATE_PATH -> ', self.template_path
            print 'PONYWHOOSH_URL_ROUTE -> ',  self.url_route

        loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader(self.template_path)
        ])

        app.jinja_loader = loader
        app.add_url_rule(
            self.url_route,
            view_func=IndexView.as_view('ponywhoosh', wh=self)
        )

    def delete_indexes(self):
        """This set to empty all the indixes registered.

        Returns:
            TYPE: This empty all the indexes.
        """
        self._indexes = {}

    def indexes(self):
        """Summary

        Returns:
            TYPE: This returns all the indexes items stored.
        """
        return [v for k, v in self._indexes.items()]

    def create_index(self, index):
        """Creates and opens index folder for given index.

        If the index already exists, it just opens it, otherwise it creates it first.

        Args:
            wh (TYPE): All the indexes stored.
        """

        index._path = os.path.join(self.indexes_path, index._name)

        if whoosh.index.exists_in(index._path):
            _whoosh = whoosh.index.open_dir(index._path)
        elif not os.path.exists(index._path):
            os.makedirs(index._path)
            _whoosh = whoosh.index.create_in(index._path, index._schema)
        index._whoosh = _whoosh

    def register_index(self, index):
        """
        Registers a given index:

        * Creates and opens an index for it (if it doesn't exist yet)
        * Sets some default values on it (unless they're already set)
        * Replaces query class of every index's model by PonyWhoosheeQuery

        Args:
            wh (TYPE): Description
        """

        self._indexes[index._name] = index
        self.create_index(index)
        return index

    def register_model(self, *fields, **kw):
        """Registers a single model for fulltext search. This basically creates
        a simple PonyWhooshIndex for the model and calls self.register_index on it.

        Args:
            *fields: all the fields indexed from the model. 
            **kw: The options for each field, sortedby, stored ... 
        """

        index = PonyWhooshIndex(pw=self)

        index._kw = kw
        index._fields = fields

        def inner(model):
            """This look for the types of each field registered in the index, whether if it is 
            Numeric, datetime or Boolean. 

            Args:
                model (TYPE): Description

            Returns:
                TYPE: Description
            """

            index._name = model._table_
            if not index._name:
                index._name  = model.__name__

            self._entities[index._name] = model

            index._schema_attrs = {}
            index._primary_key = None
            index._primary_key_type = int

            lista = {} # FIX: the name, is not helpful
            for field in model._attrs_:
                if field == model._pk_:
                    index._primary_key = field.name
                    index._primary_key_type = field.py_type
                    index._schema_attrs[field.name] = whoosh.fields.ID(stored=True, unique=True)

                if field.name in index._fields:
                    if field.is_string == False and field.is_relation == False:
                        if field.py_type.__name__ in ['int', 'float']:
                            index._schema_attrs[field.name] = whoosh.fields.NUMERIC(**kw)
                        elif field.py_type.__name__ == 'datetime':
                            index._schema_attrs[field.name] = whoosh.fields.DATETIME(**kw)
                        elif field.py_type.__name__ == 'bool':
                            index._schema_attrs[field.name] = whoosh.fields.BOOLEAN(stored=True)
                        lista[field.name] = field.py_type.__name__
                    else:
                        index._schema_attrs[field.name] = whoosh.fields.TEXT(**kw)

            index._schema = whoosh.fields.Schema(**index._schema_attrs)

            self.register_index(index)

            def _middle_save_(obj, status):
                """Summary

                Args:
                    obj (TYPE): Description
                    status (TYPE): Description

                Returns:
                    TYPE: Description
                """
                writer = index._whoosh.writer(timeout=self.writer_timeout)

                attrs = {index._primary_key: obj.get_pk()}
                for f in index._schema_attrs.keys():
                    attrs[f] = getattr(obj, f)

                    try:
                        attrs[f] = unicode(attrs[f])
                    except Exception, e:
                        print e

                    if attrs[f] in ['None', 'nan']:
                        attrs[f] = u'0'

                    if f in lista:
                        attrs[f] = getattr(obj, f)

                if status == 'inserted':
                    writer.add_document(**attrs)
                elif status == 'updated':
                    writer.update_document(**attrs)
                elif status in set(['marked_to_delete', 'deleted', 'cancelled']):
                    writer.delete_by_term(primary, attrs[primary])

                writer.commit()
                return obj._after_save_

            model._after_save_ = _middle_save_
            model._pw_index_ = index
            index._model = model
            return model
        return inner

    @orm.db_session
    def search(self, *arg, **kw):
        """Search function. This allows you to search using the following arguments.

        Args:
            *arg: The search string. 
            **kw: The options available for searching: include_entity, add_wildcards, something, 
            fields, except_fields, etc. These options were described previously. 

        Returns:
            TYPE: Description
        """
        output = {
            'runtime': 0,
            'results': {},
            'matched_terms': defaultdict(set),
            'cant_results': 0
        }

        indexes = self.indexes()

        models = kw.get('models', self._entities.values())
        models = [self._entities.get(model, None) if isinstance(model, str) or isinstance(model, unicode)
                  else model for model in models]
        models = filter(lambda x: x is not None, models)

        if models == [] or not models:
            models = self._entities.values()

        if self.debug:
            print "SEARCHING ON MODELS -> ", models

        indexes = [m._pw_index_ for m in models if hasattr(m, '_pw_index_')]

        if indexes == []:
            return output

        runtime, cant = 0, 0

        ma = defaultdict(set)
        for index in indexes:
            res = index.search(*arg, **kw)
            runtime += res['runtime']
            cant += res['cant_results']

            output['results'][index._path] = {
                'items': res['results'],
                'matched_terms': res['matched_terms']
            }
            for k, ts in res['matched_terms'].items():
                for t in ts:
                    ma[k].add(t)

        output['runtime'] = runtime
        output['matched_terms'] = {k: list(v) for k, v in ma.items()}
        output['cant_results'] = cant
        return output
