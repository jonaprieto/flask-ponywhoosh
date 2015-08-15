import sys
import os
import re
import abc
from pony import orm
import whoosh
from whoosh import qparser
from whoosh import fields, index


class Whoosheer(object):

    """

    Whoosheer is basically a unit of fulltext search. It represents either of:

    * One table, in which case all given fields of the model is searched.
    * More tables, in which case all given fields of all the tables are searched.
    """

    def search(self, search_string, values_of='', group=qparser.OrGroup, match_substrings=True, limit=None):
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
        prepped_string = self.prep_search_string(
            search_string, match_substrings)
        with self.index.searcher() as searcher:
            parser = whoosh.qparser.MultifieldParser(
                self.schema.names(), self.index.schema, group=group)
            query = parser.parse(prepped_string)
            results = searcher.search(query, limit=limit)
            result_set = set()
            result_ranks = {}
            print results[:]
            print self.primary
            for rank, result in enumerate(results):
                  pk = result[self.primary]
                  result_set.add(pk)
                  result_ranks[pk] = rank

            with orm.db_session:
                print result_set
                f = []
                # The following code even thought is long, 
                #is the only one that works, because the 
                #shorcuts from pony allways raise errors. 
                for ent in self.model.select():
                    if ent.get_pk() in result_set:
                        f.append(ent)
                f.sort(key=lambda x: result_ranks[x.get_pk()])
               

                return f 
            
            return  


        

    def prep_search_string(self, search_string, match_substrings):
        """Prepares search string as a proper whoosh search string."""
        s = search_string.strip()
        # we don't want stars from user
        s = s.replace('*', '')
        if len(s) < self.search_string_min_len:
            raise ValueError('Search string must have at least {} characters'.format(
                self.search_string_min_len))

        if match_substrings:
            s = u'*{0}*'.format(re.sub('[\s]+', '* *', s))
        return s


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
        return wh

    def register_model(self, *index_fields, **kw):
        """Registers a single model for fulltext search. This basically creates
        a simple Whoosheer for the model and calls self.register_whoosheer on it.
        """

        if self.debug:
            print 'ModelWhoosheer created'
            print 'index_fields', index_fields
            print 'kw', kw

        mwh = Whoosheer()
        # print "*"*100, mwh.searhc

        def inner(model):
            mwh.index_subdir = model._table_
            if not mwh.index_subdir:
                mwh.index_subdir = model.__name__

            schema_attrs = {}
            mwh.primary = None
    
            for field in model._attrs_:
                if field == model._pk_:
                    mwh.primary = field.name

                    if isinstance(field.py_type, 
                    ( orm.unicode, orm.LongUnicode, orm.LongStr, str)):
                        schema_attrs[field.name] = whoosh.fields.ID(
                            stored=True, unique=True)
                    else: 
                        schema_attrs[field.name] = whoosh.fields.NUMERIC(
                            stored=True, unique=True)


                elif field.name in index_fields and isinstance(field.py_type, 
                    ( type(orm.unicode), type(orm.LongUnicode), type(orm.LongStr), type(str))):

                    schema_attrs[field.name] = whoosh.fields.TEXT(**kw)

            mwh.schema = whoosh.fields.Schema(**schema_attrs)
            mwh._is_model_whoosheer = True

            if self.debug:
                print '>> schema_attrs:', schema_attrs

            def _middle_save_(obj, status):
                writer = mwh.index.writer(timeout=self.writer_timeout)

                attrs = {mwh.primary: obj.get_pk()}
                for f in schema_attrs.keys():
                    attrs[f] = getattr(obj, f)

                if status == 'inserted':
                    writer.add_document(**attrs)
                elif status == 'updated':
                    writer.update_document(**attrs)
                elif status in set(['marked_to_delete', 'deleted', 'cancelled']):
                    writer.delete_by_term(primary, attrs[primary])

                if self.debug:
                    print 'writer>', writer
                    print 'obj>', obj,  '/' * 30, obj._status_
                    print 'cantidad>', mwh.index.doc_count()
                    print 'attrs>', attrs

                writer.commit(optimize=True)
                return obj._after_save_

            self.register_whoosheer(mwh)

            model._after_save_ = _middle_save_
            model._whoosheer_ = mwh
            model._whoosh_index_ = mwh.index
            model._whoosh_search_ = mwh.search
            mwh.model = model

            return model
        return inner


def search(model, *arg, **kw):
    return model._whoosh_search_(*arg, **kw)
