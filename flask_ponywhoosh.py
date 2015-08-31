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
from collections import defaultdict


class Whoosheer(object):

    """

    Whoosheer is basically a unit of fulltext search.

    """

    def add_field(self, fieldname, fieldspec=fields.TEXT):
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

    def counts(self):
        return self.index.doc_count()

    @orm.db_session
    def charge_documents(self):
        doc_count = self.index.doc_count()
        objs = orm.count(e for e in self.model)

        field_names = set(self.schema_attrs.keys())
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

    def update_documents(self):
        self.delete_documents()
        self.charge_documents()

    @orm.db_session
    def search(self, search_string, **opt):
        prepped_string = self.prep_search_string(
            search_string, opt.get('add_wildcards', False))
        with self.index.searcher() as searcher:
            parser = whoosh.qparser.MultifieldParser(
                self.schema.names(), self.index.schema,
                group=opt.get('group', qparser.OrGroup))

            if 'field' in opt:
                if isinstance(opt['field'], str) or isinstance(opt['field'], unicode):
                    parser = whoosh.qparser.QueryParser(
                        opt['field'], self.index.schema)
                elif isinstance(opt['field'], list):
                    opt['fields'] = opt.get('fields', []) + opt['field']

            if 'fields' in opt:
                fields_parser = opt.get('fields', self.schema.names())
                fields_parser = list(
                    set(opt['fields']) & set(self.schema.names()))

                parser = whoosh.qparser.MultifieldParser(
                    fields_parser, self.index.schema,
                    group=opt.get('group', qparser.OrGroup))

            query = parser.parse(prepped_string)

            parameters = [
                'collapse', 'collapse_limit', 'collapse_order',
                'filter', 'groupedby', 'limit', 'maptype', 'mask',
                'optimize', 'reverse', 'scored', 'sortedby', 'terms'
            ]

            search_opts = {k: v for k, v in opt.items() if k in parameters}
            results = searcher.search(query, terms=True, **search_opts)

            ma = defaultdict(set)
            for f, term in results.matched_terms():
                ma[f].add(term)

            dic = {
                'runtime': results.runtime,
                'cant_results': results.estimated_length(),
                'matched_terms': {k: list(v) for k, v in ma.items()},
                'facet_names': results.facet_names(),
            }
            rs = []
            pk = unicode(self.primary)
            for r in results:
                parms = {pk: r[pk]}
                entity = self.model.get(**parms)
                ans = {
                    'result': entity,
                    'rank': r.rank,
                    'score': r.score,
                    'docnum': r.docnum
                }
                rs.append(ans)
            dic['results'] = rs

            if dic['cant_results'] == 0 and opt.get('something', False):
                opt['add_wildcards'] = True
                opt['something'] = False
                return self.search(search_string, **opt)
            return dic

    def prep_search_string(self, search_string, add_wildcards=False):
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
        if add_wildcards:
            s = u'*{0}*'.format(re.sub('[\s]+', '* *', s))
        return s


class Whoosh(object):

    """A top level class that allows to register whoosheers."""

    _whoosheers = {}
    index_path_root = 'whooshee'
    search_string_min_len = 3
    writer_timeout = 2

    def __init__(self, app=None):

        if app:
            self.init_app(app)
        if not os.path.exists(self.index_path_root):
            os.makedirs(self.index_path_root)

    def init_app(self, app):

        self.index_path_root = app.config.get('WHOOSHEE_DIR', '') or 'whooshee'
        self.search_string_min_len = app.config.get(
            'WHOSHEE_MIN_STRING_LEN', 3)
        self.writer_timeout = app.config.get('WHOOSHEE_WRITER_TIMEOUT', 2)

    def whoosheers(self):
        return [v for k, v in self._whoosheers.items()]

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

        self._whoosheers[wh.index_subdir] = wh
        self.create_index(wh)
        return wh

    def register_model(self, *index_fields, **kw):
        """Registers a single model for fulltext search. This basically creates
        a simple Whoosheer for the model and calls self.register_whoosheer on it.
        """

        mwh = Whoosheer()
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
                    except Exception, e:
                        print e

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

    @orm.db_session
    def search(self, *arg, **kw):
        full_results = {'runtime': 0,
                        'results': {},
                        'matched_terms': defaultdict(set),
                        'cant_results': 0
                        }
        whoosheers = self.whoosheers()
        if 'models' in kw:
            models = kw['models']
            whoosheers = []
            for model in models:
                if hasattr(model, '_wh_'):
                    whoosheers.append(model._wh_)

        if whoosheers == []:
            return full_results

        runtime, cant = 0, 0

        ma = defaultdict(set)
        for whoosher in whoosheers:
            output = whoosher.search(*arg, **kw)
            runtime += output['runtime']
            cant += output['cant_results']

            full_results['results'][whoosher.index_subdir] = {
                'items': output['results'],
                'matched_terms': output['matched_terms']
            }
            for k, ts in output['matched_terms'].items():
                for t in ts:
                    ma[k].add(t)

        full_results['runtime'] = runtime
        full_results['matched_terms'] = {k: list(v) for k, v in ma.items()}
        full_results['cant_results'] = cant
        return full_results

@orm.db_session
def search(model, *arg, **kw):
    return model._wh_.search(*arg, **kw)


@orm.db_session
def delete_field(model, *arg):
    return model._wh_.delete_field(*arg)

def full_search(wh, *arg, **kw):
    return wh.search(*arg, **kw)
