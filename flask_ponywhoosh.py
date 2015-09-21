'''

    flask_ponywhoosh extension
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Adds capabilities to perform full-text search over your modules of Pony ORM
    for flask applications. Enjoy it! 

    :copyright: (c) 2015 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
    :license: BSD (see LICENSE.md)

'''

from collections import defaultdict
from datetime import datetime
import os
import re
import sys

from __version__ import __version__
from pony import orm
from whoosh import fields, index, qparser
import whoosh


class Whoosheer(object):

    """

    Whoosheer is basically a unit of fulltext search.

    """

    parameters = {
        'limit': 0,
        'optimize': False,
        'reverse': False,
        'scored': u'',
        'sortedby': u'',
    }

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

    def optimize(self):
        self.index.optimize()

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
            writer.commit()

    def update_documents(self):
        self.delete_documents()
        self.charge_documents()

    @orm.db_session
    def search(self, search_string, **opt):
        prepped_string = self.prep_search_string(
            search_string, self.to_bool(opt.get('add_wildcards', False)))

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
            search_opts = self.parse_opts_searcher(opt, self.parameters)
            results = searcher.search(query,terms=True,**search_opts)

            ma = defaultdict(set)
            for f, term in results.matched_terms():
                ma[f].add(term)

            dic = {
                'runtime': results.runtime,
                'cant_results': results.estimated_length(),
                'matched_terms': {k: list(v) for k, v in ma.items()},
                'facet_names': results.facet_names(),
            }

            dic['results'] = []
            pk = unicode(self.primary)
            for r in results:
                ans = {
                    'pk': r[pk],
                    'rank': r.rank,
                    'score': r.score,
                    'docnum': r.docnum
                }
                if self.to_bool(opt.get('include_entity', False)):
                    parms = {pk: r[pk]}
                    entity = self.model.get(**parms)
                    ans['entity'] = entity.to_dict()
                dic['results'].append(ans)

            if dic['cant_results'] == 0 and self.to_bool(opt.get('something', False)):
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

    def to_bool(self, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, unicode) or isinstance(v, str):
            return v == 'True' or v == 'true' or v == 't' or v == 'y' or v == 'yes'
        if isinstance(v, int):
            return bool(v)
        return False

    def parse_opts_searcher(self, opts, parameters):
        assert isinstance(opts, dict)
        res = {}
        for k, v in opts.items():
            if k in parameters:
                typevalue = parameters[k]
                if isinstance(typevalue, int):
                    if isinstance(v, list):
                        res[k] = v[0]
                    res[k] = int(v)
                elif isinstance(typevalue, unicode):
                    if isinstance(v, list):
                        res[k] = v[0]
                    res[k] = unicode(v)
                elif isinstance(typevalue, bool):
                    if isinstance(v, list):
                        res[k] = v[0]
                    res[k] = self.to_bool(v)
        return res


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
        self.index_path_root = app.config.get('WHOOSHEE_DIR',  'whooshee')
        self.search_string_min_len = app.config.get(
            'WHOSHEE_MIN_STRING_LEN', 3)
        self.writer_timeout = app.config.get('WHOOSHEE_WRITER_TIMEOUT', 2)

    def init_opts(self, opts):
        assert isinstance(opts, dict)
        self.index_path_root = opts.get('WHOOSHEE_DIR',  'whooshee')
        self.search_string_min_len = opts.get(
            'WHOSHEE_MIN_STRING_LEN', 3)
        self.writer_timeout = opts.get('WHOOSHEE_WRITER_TIMEOUT', 2)
        

    def delete_whoosheers(self):
        self._whoosheers = {}

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

            lista = {}
            for field in model._attrs_:
                if field == model._pk_:
                    mwh.primary = field.name
                    mwh.primary_type = field.py_type

                    mwh.schema_attrs[field.name] = whoosh.fields.ID(
                        stored=True, unique=True)

                if field.name in index_fields:
                    if field.is_string == False and field.is_relation == False:
                        if field.py_type.__name__ in ['int', 'float']:
                            mwh.schema_attrs[
                                field.name] = whoosh.fields.NUMERIC(**kw)
                        elif field.py_type.__name__ == 'datetime':
                            mwh.schema_attrs[
                                field.name] = whoosh.fields.DATETIME(**kw)
                        elif field.py_type.__name__=='bool':
                            mwh.schema_attrs[
                                field.name] = whoosh.fields.BOOLEAN(stored=True)
                        lista[field.name] = field.py_type.__name__
                    else:

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
