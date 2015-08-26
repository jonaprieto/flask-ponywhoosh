'''

    flask_ponywhoosh extension
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Adds capabilities to perform text search over your modules of Pony ORM
    for flask applications.

    :copyright: (c) 2015 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
    :license: BSD (see LICENSE.md)

'''

import abc
import os
import re
import sys

from pony import orm
from whoosh import fields, index
from whoosh import qparser
import whoosh


class Whoosheer(object):

    """

    Whoosheer is basically a unit of fulltext search.

    """

    def search(self, search_string, **opt):
        prepped_string = self.prep_search_string(search_string)
        with self.index.searcher() as searcher:
            parser = whoosh.qparser.MultifieldParser(
                self.schema.names(), self.index.schema,
                group=opt.get('group', qparser.OrGroup))
            query = parser.parse(prepped_string)

            search_opts = {}
            parameters = ['limit', 'scored', 'sortedby',
                          'reverse', 'groupedby', 'optimize', 'filter', 'mask', 'terms', 'maptype', 'collapse', 'collapse_limit', 'collapse_order']

            for o in opt.keys():
                if o in parameters:
                    search_opts[o] = opt[o]

            results = searcher.search(query, terms=True, **search_opts)
            result_set = set()
            result_ranks = {}
            for rank, result in enumerate(results):
                pk = result[self.primary]
                result_set.add(pk)
                result_ranks[pk] = rank
            dic = {'runtime':results.runtime,'results':results.docs(),
                        'cant_results':results.estimated_length(),
                            'matched_terms':results.matched_terms(),
                            'facet_names':results.facet_names(), 'score':list(results.items())}
            

            with orm.db_session:
                rs = []
                # The following code even thought is long,
                # is the only one that works, because the
                # shorcuts from pony always raise errors.
                for ent in self.model.select():
                    if unicode(ent.get_pk()) in result_set:
                        rs.append(ent)
                rs.sort(key=lambda x: result_ranks[unicode(x.get_pk())])
                dic['results'] = rs
                return dic
            return dic




    def prep_search_string(self, search_string):
        """Prepares search string as a proper whoosh search string."""
        s = search_string.strip()
        try:
            s = unicode(s)
        except:
            pass
        # we don't want stars from user
        s = s.replace('*', '')
        if len(s) < self.search_string_min_len:
            raise ValueError('Search string must have at least {} characters'.format(
                self.search_string_min_len))

        # s = u'*{0}*'.format(re.sub('[\s]+', '* *', s))
        return s

    @orm.db_session
    def _charge_data_(self):
        ix = self.model._whoosh_index_
        doc_count = ix.doc_count()
        objs = orm.count(e for e in self.model)
        print 'charge_data() ', '-' * 50
        print 'doc_count =', doc_count
        print 'objs = ', objs

        if doc_count == 0 and objs > 0:
            writer = self.index.writer()
            for obj in orm.select(e for e in self.model):
                attrs = {self.primary: obj.get_pk()}
                for f in self.schema_attrs.keys():
                    attrs[f] = unicode(getattr(obj, f))
                writer.add_document(**attrs)
            writer.commit(optimize=True)


    def _delete_index_(self):

        ix = self.model._whoosh_index_
        sch = ix.schema 
        field_name=sch.names()
        for s in field_name:
            del_name= s
            ix.remove_field(del_name)
    def _delete_index_by_field_(self,field_name):
        ix = self.model._whoosh_index_
        t=field_name.strip()
        ix.remove_field(t)
        return ix.schema


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

        def inner(model):
            mwh.index_subdir = model._table_
            if not mwh.index_subdir:
                mwh.index_subdir = model.__name__

            mwh.schema_attrs = {}
            mwh.primary = None
            mwh.primary_type = int

            for field in model._attrs_:
                if field == model._pk_:
                    mwh.primary = field.name
                    mwh.primary_type = field.py_type

                    mwh.schema_attrs[field.name] = whoosh.fields.ID(
                        stored=True, unique=True)
                if field.name in index_fields:
                    mwh.schema_attrs[field.name] = whoosh.fields.TEXT(**kw)

            mwh.schema = whoosh.fields.Schema(**mwh.schema_attrs)
            mwh._is_model_whoosheer = True

            if self.debug:
                print '>> mwh.schema_attrs:', mwh.schema_attrs

            def _middle_save_(obj, status):
                writer = mwh.index.writer(timeout=self.writer_timeout)

                attrs = {mwh.primary: obj.get_pk()}
                for f in mwh.schema_attrs.keys():
                    attrs[f] = getattr(obj, f)
                    try:
                        attrs[f] = unicode(attrs[f])
                    except:
                        pass

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
            model._whoosh_charge_data_ = mwh._charge_data_
            model._whoosh_delete_index_ =mwh._delete_index_
            model._whoosh_delete_index_by_field_=mwh._delete_index_by_field_
            mwh.model = model
        

            return model
        return inner


def search(model, *arg, **kw):
    return model._whoosh_search_(*arg, **kw)
def delete(model,*arg):
    return model._whoosh_delete_index_by_field_(*arg)

def full_search(ind,*arg,**kw):
    full_results={'results':[],'matched_terms':[]}

    for whoosher in ind.whoosheers: 
        resul = whoosher.search(arg[0])
        full_results['results'].extend(resul['results'])
        full_results['matched_terms'].extend(resul['matched_terms'])
    
    return full_results
