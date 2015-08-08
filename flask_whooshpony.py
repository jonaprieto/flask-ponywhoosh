import sys
import os
import re
import abc
from pony.orm import *

import whoosh
from whoosh import qparser


class AbstractWhoosheer(object):

    """A superclass for all whoosheers.

    Whoosheer is basically a unit of fulltext search. It represents either of:

    * One table, in which case all given fields of the model is searched.
    * More tables, in which case all given fields of all the tables are searched.
    """

    @classmethod
    def search(cls, search_string, values_of='', group=qparser.OrGroup, match_substrings=True, limit=None):
        """Actually searches the fields for given search_string.

        Args:
            search_string: string to search for
            values_of: if given, the method will not return the whole records, but only values
                       of given column (defaults to returning whole records)
            group: whoosh group to use for searching, defaults to OrGroup (searches for all
                   words in all columns)
            match_substrings: True if you want to match substrings, False otherwise
            limit: number of the top records to be returned, default None returns all records

        Returns:
            Found records if 'not values_of', else values of given column
        """
        prepped_string = cls.prep_search_string(
            search_string, match_substrings)
        with cls.index.searcher() as searcher:
            parser = whoosh.qparser.MultifieldParser(
                cls.schema.names(), cls.index.schema, group=group)
            query = parser.parse(prepped_string)
            results = searcher.search(query, limit=limit)
            if values_of:
                return [x[values_of] for x in results]
            return results

    @classmethod
    def prep_search_string(cls, search_string, match_substrings):
        """Prepares search string as a proper whoosh search string."""
        s = search_string.strip()
        # we don't want stars from user
        s = s.replace('*', '')
        if len(s) < cls.search_string_min_len:
            raise ValueError('Search string must have at least {} characters'.format(
                cls.search_string_min_len))
        # replace multiple with star space star
        if match_substrings:
            s = u'*{0}*'.format(re.sub('[\s]+', '* *', s))
        # TODO: some sanitization
        return s

AbstractWhoosheerMeta = abc.ABCMeta(
    'AbstractWhoosheer', (AbstractWhoosheer,), {})


class Whoosh(object):

    """A top level class that allows to register whoosheers."""

    whoosheers = []
    index_path_root = 'whooshee'
    search_string_min_len = 3
    writer_timeout = 2

    debug = False

    def __init__(self, app=None, debug=False):

        self.debug = debug
        if app:
            self.init_app(app)
        if not os.path.exists(self.index_path_root):
            os.makedirs(self.index_path_root)

    def init_app(self, app):

        self.index_path_root = app.config.get('WHOOSHEE_DIR', '') or 'whooshee'
        self.search_string_min_len = app.config.get(
            'WHOSHEE_MIN_STRING_LEN', 3)
        self.writer_timeout = app.config.get('WHOOSHEE_WRITER_TIMEOUT', 2)

        # models_committed.connect(self.on_commit, sender=app)

    def create_index(self, wh):
        """Creates and opens index for given whoosheer.

        If the index already exists, it just opens it, otherwise it creates it first.
        """
        index_path = os.path.join(self.index_path_root, wh.index_subdir)
        if whoosh.index.exists_in(index_path):
            if self.debug:
                print 'existe el indice para whoosh'
            index = whoosh.index.open_dir(index_path)
        else:
            if self.debug:
                print 'se creo el indice para whoosh'
            if not os.path.exists(index_path):
                os.makedirs(index_path)
            index = whoosh.index.create_in(index_path, wh.schema)
        wh.index = index

    def register_whoosheer(self, wh):
        """Registers a given whoosheer:

        * Creates and opens an index for it (if it doesn't exist yet)
        * Sets some default values on it (unless they're already set)
        * Replaces query class of every whoosheer's model by WhoosheeQuery
        """
        if self.debug:
            print 'register_whoosheer'
        if not hasattr(wh, 'search_string_min_len'):
            wh.search_string_min_len = self.search_string_min_len
        if not hasattr(wh, 'index_subdir'):
            wh.index_subdir = wh.__name__

        self.__class__.whoosheers.append(wh)
        self.create_index(wh)
        # for model in wh.models:
        #     model.query_class = WhoosheeQuery
        return wh

    def register_model(self, *index_fields, **kw):
        """Registers a single model for fulltext search. This basically creates
        a simple Whoosheer for the model and calls self.register_whoosheer on it.
        """
        # construct subclass of AbstractWhoosheer for a model
        class ModelWhoosheer(AbstractWhoosheerMeta):
            pass

        if self.debug:
            print 'ModelWhoosheer created'
        if self.debug:
            print 'index_fields', index_fields
        if self.debug:
            print 'kw', kw
        mwh = ModelWhoosheer

        def inner(model):
            if self.debug:
                print '>>> inner'
            mwh.index_subdir = model._table_
            if not mwh.index_subdir:
                mwh.index_subdir = model.__name__

            mwh.models = [model]
            if self.debug:
                print '>>> table:', mwh.index_subdir

            schema_attrs = {}
            primary = None
            for field in model._attrs_:
                if field == model._pk_:
                    primary = field.name
                    if isinstance(field.py_type, type(int)):
                        schema_attrs[field.name] = whoosh.fields.NUMERIC(
                            stored=True, unique=True)
                    else:
                        schema_attrs[field.name] = whoosh.fields.TEXT(
                            stored=True)
                else:
                    if field.name in index_fields:
                        schema_attrs[field.name] = whoosh.fields.TEXT(**kw)

            mwh.schema = whoosh.fields.Schema(**schema_attrs)
            mwh._is_model_whoosheer = True

            if self.debug:
                print '>> schema_attrs:', schema_attrs

            self.register_whoosheer(mwh)

            def operation(model, op):
                writer = mwh.index.writer(timeout=self.writer_timeout)
                if self.debug:
                    print 'writer>', writer
                    print model,  '/' * 30, model._status_
                    print 'model>', model

                attrs = {primary: model._pk_}
                for f in schema_attrs.keys():
                    attrs[f] = getattr(model, f)
                    if not isinstance(attrs[f], int):
                        if sys.version < '3':
                            attrs[f] = unicode(attrs[f])
                        else:
                            attrs[f] = str(attrs[f])

                if op == 'created':
                    writer.add_document(**attrs)
                elif op == 'modified':
                    writer.update_document(**attrs)
                elif op == 'mark_to_delete':
                    pass

                writer.commit(optimize=True)
                if self.debug:
                    print '>>>@ ', attrs

            def saving(obj):
                status = obj._status_
                try:
                    operation(obj, status)
                except Exception, e:
                    if self.debug:
                        print e
                return obj._before_save_

            model._before_save_ = saving
            model._whoosheer_ = mwh
        #     model.whoosh_search = mwh.search
            return model
        return inner
