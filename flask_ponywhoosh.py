'''

    flask_ponywhoosh extension
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Adds capabilities to perform text search over your modules of Pony ORM
    for flask applications.

    :copyright: (c) 2015 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
    :license: BSD (see LICENSE.md)

'''

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

    def __init__(self):
        # .. construir el indice..

    def add_field(self, fieldname, fieldspec):
        self.index.add_field(fieldname, fieldspec)
        return self.index.schema

    def delete_field(self, field_name):
        self.index.remove_field(field_name.strip())
        return self.index.schema

    def delete_documents(self):
        pk = unicode(self.primary)
        for doc in self.index.searcher().documents():
            if pk in doc:
                doc_pk = unicode(doc[pk])
                self.index.delete_by_term(pk, doc_pk)

    @orm.db_session
    def charge_documents(self):
        doc_count = self.index.doc_count()
        objs = orm.count(e for e in self.model)

        field_names = set(self.model.schema_attrs.keys())
        missings = set(self.index.schema.names())

        for f in list(field_names - missings):
            self.add_field(f, fields.TEXT(self.kw))

        if doc_count == 0 and objs > 0:
            writer = self.index.writer()
            for obj in orm.select(e for e in self.model):
                attrs = {self.primary: obj.get_pk()}
                for f in self.schema_attrs.keys():
                    attrs[f] = unicode(getattr(obj, f))
                writer.add_document(**attrs)
            writer.commit(optimize=True)
        else:
            update_documents()

    def update_documents(self):
        self.delete_documents()
        self.charge_documents()

    def search(self, search_string, **opt):
        prepped_string = self.prep_search_string(search_string)
        with self.index.searcher() as searcher:
            parser = whoosh.qparser.MultifieldParser(
                self.schema.names(), self.index.schema,
                group=opt.get('group', qparser.OrGroup))
            query = parser.parse(prepped_string)

            search_opts = {}
            parameters = [
                'collapse', 'collapse_limit', 'collapse_order',
                'filter', 'groupedby', 'limit', 'maptype', 'mask',
                'optimize', 'reverse', 'scored', 'sortedby', 'terms'
            ]

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

            dic = {
                'runtime': results.runtime,
                'results': results.docs(),
                'cant_results': results.estimated_length(),
                'matched_terms': results.matched_terms(),
                'facet_names': results.facet_names(),
                'score': list(results.items())
            }

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
        s = s.replace('*', '')
        if len(s) < self.search_string_min_len:
            raise ValueError('Search string must have at least {} characters'.format(
                self.search_string_min_len))
        s = u'*{0}*'.format(re.sub('[\s]+', '* *', s))
        return s


class Whoosh(object):

    """A top level class that allows to register whoosheers."""

    whoosheers = []
    index_path_root = 'whooshee'
    search_string_min_len = 3
    writer_timeout = 2

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
            index = whoosh.index.open_dir(index_path)
        else:
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

        mwh = Whoosheer(debug=self.debug)
        mwh.kw = kw

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
            self.register_whoosheer(mwh)

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

                writer.commit(optimize=True)
                return obj._after_save_

            model._after_save_ = _middle_save_
            model._wh_ = mwh
            mwh.model = model
            return model
        return inner


def search(model, *arg, **kw):
    return model._wh_.search(*arg, **kw)


def delete_field(model, *arg):
    return model._wh_.delete_field(*arg)


def full_search(ind, *arg, **kw):
    full_results = {'results': [], 'matched_terms': []}

    for whoosher in ind.whoosheers:
        resul = whoosher.search(arg[0])
        full_results['results'].extend(resul['results'])
        full_results['matched_terms'].extend(resul['matched_terms'])

    return full_results
