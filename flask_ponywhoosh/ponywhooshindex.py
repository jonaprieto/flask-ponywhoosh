#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: d555

"""

    PonyWhooshIndex Class
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2015-2016 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
    :license: BSD (see LICENSE.md)

"""

from pony import orm
from whoosh import fields as whoosh_module_fields
from whoosh import qparser
from collections import defaultdict
import whoosh 
import re

class PonyWhooshIndex(object):

    debug = False
    _parameters = {
        'limit': 0,
        'optimize': False,
        'reverse': False,
        'scored': u'',
        'sortedby': u'',
    }

    @property
    def whoosh(self):
        return self._whoosh

    @property
    def path(self):
        return self._path

    @property
    def schema(self):
        return self._schema

    @property
    def name(self):
        return self._name

    @property
    def fields(self):
        return self._fields

    def __init__(self, pw):
        """Summary

        Args:
            wh (PonyWhoosh): Initializes of index. 
        """
        self._pw = pw
        self.debug = pw.debug

    def add_field(self, fieldname, fieldspec=whoosh_module_fields.TEXT):
        """Add Field

        Args:
            fieldname (Text): This parameters register a new field in specified model.
            fieldspec (Name, optional): This option adds various options as were described before. 

        Returns:
            TYPE: The new schema after deleted is returned. 
        """
        self._whoosh.add_field(fieldname, fieldspec)
        return self._whoosh.schema

    def delete_field(self, field_name):
        """This function deletes one determined field using the command MODEL.wh.delete_field(FIELD)

        Args:
            field_name (string): This argument let you delete some field for some model registered in the index. 

        Returns:
            INDEX: The new schema after deleted is returned. 
        """
        self._whoosh.remove_field(field_name.strip())
        return self._whoosh.schema

    def delete_documents(self):
        """
        Deletes all the  documents using the  pk associated to them. 

        Returns:
            The new index with the document deleted. 
        """
        pk = unicode(self._primary_key)
        for doc in self._whoosh.searcher().documents():
            if pk in doc:
                doc_pk = unicode(doc[pk])
                self._whoosh.delete_by_term(pk, doc_pk)

    def optimize(self):
        """ The index is reindexed, optimizing the run time of searchings and space used. Everytime a document is added a new file would be created, but optimizing would reduce all to just one. 


        Returns:
            TYPE: Index optimized. 
        """
        self._whoosh.optimize()

    def counts(self):
        """This method counts all the documents contained in  a certain registered model. 

        Returns:
            Int: A number with all the documents a model have. 
        """
        return self._whoosh.doc_count()

    @orm.db_session
    def charge_documents(self):
        """
        This method allow you to charge documents you already have 
            in your database. In this way an Index would be created according to 
            the model and fields registered. 

        Returns:
            An index updated with new documents.  
        """
        doc_count = self._whoosh.doc_count()
        objs = orm.count(e for e in self._model)

        field_names = set(self._schema_attrs.keys())
        missings = set(self._whoosh.schema.names())

        for f in list(field_names - missings):
            self.add_field(f, fields.TEXT(self.kw))

        if doc_count == 0 and objs > 0:
            writer = self._whoosh.writer()
            for obj in orm.select(e for e in self._model):
                attrs = {self._primary_key: obj.get_pk()}
                for f in self._schema_attrs.keys():
                    attrs[f] = unicode(getattr(obj, f))
                writer.add_document(**attrs)
            writer.commit()

    def update_documents(self):
        """It deletes all the documents in the index and charge them again. 

        Returns:
            Index: with updated documents"""
        self.delete_documents()
        self.charge_documents()

    @orm.db_session
    def search(self, search_string, **opt):
        """The core function of the package. These are the arguments we consider.  


        Args:
            search_string (str): This is what you are looking for in your pony database. 
            opt: The following opts are available for the search function: 
            * add_wildcars(bool): This opt allows you to search no literal queries. 
            * fields: This opt let you filter your search result on some model by the fields you want to search.
            * include_entity: This opt let you see not only the result and the register fields but all the instance from the entity of the database. 
            * except_fields: Tell the searcher to not look on these fields. 
            * use_dict: This option let you activate the dict for the items in the search result, or just view them as a list. 
            We implement this because we wanted that the  first field registered of the model would be the most important one. 
            As was explained in the IndexView section. 
        Returns:
            dict: Description
        """
        if self.debug:
            print 'VERSION -> ', __version__
            print 'opt:'
            pprint(opt)

        prepped_string = self.prep_search_string(
            search_string, self.to_bool(opt.get('add_wildcards', False)))

        with self._whoosh.searcher() as searcher:

            fields = opt.get('fields', self._schema.names())
            fields = filter(lambda x: len(x) > 0, fields)

            field = opt.get('field', '')
            if len(field) > 0:
                if isinstance(field, str) or isinstance(field, unicode):
                    fields = [field]
                elif isinstance(field, list):
                    fields = fields + field

            fields = filter(lambda x: len(x) > 0, fields)

            if len(fields) == 0:
                fields = self._schema.names()

            if len(fields) > 0:
                fields = set(fields) & set(self._schema.names())
                fields = list(fields)

            except_fields = opt.get('except_fields', [])
            except_fields = filter(lambda x: len(x) > 0, except_fields)

            if len(except_fields) > 0:
                fields = list(set(fields) - set(except_fields))

            parser = whoosh.qparser.MultifieldParser(
                fields, self._whoosh.schema,
                group=opt.get('group', qparser.OrGroup))

            query = parser.parse(prepped_string)
            search_opts = self.parse_opts_searcher(opt, self._parameters)
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

            dic['results'] = []
            pk = unicode(self._primary_key)
            for r in results:
                ans = {
                    'pk': r[pk],
                    'rank': r.rank,
                    'score': r.score,
                    'docnum': r.docnum
                }
                if self.to_bool(opt.get('include_entity', False)):
                    parms = {pk: r[pk]}
                    entity = self._model.get(**parms)
                    dic_entity = entity.to_dict()
                    if opt.get('use_dict', True):
                        ans['entity'] = dic_entity
                    else:
                        fields_missing = set(
                            dic_entity.keys()) - set(self._fields)
                        ans['other_fields'] = [(k, dic_entity[k])
                                               for k in fields_missing]
                        ans['entity'] = [(k, dic_entity[k])
                                         for k in self._fields]
                    ans['model'] = self._name
                dic['results'].append(ans)

            if dic['cant_results'] == 0 and self.to_bool(opt.get('something', False)):
                opt['add_wildcards'] = True
                opt['something'] = False
                return self.search(search_string, **opt)
            return dic

    def prep_search_string(self, search_string, add_wildcards=False):
        """Prepares search string as a proper whoosh search string.

        Args:
            search_string (str): it prepares the search string and see if the lenght is correct. 
            add_wildcards (bool, optional): It runs a query for inexact queries. 

        Raises:
            ValueError: When the search string does not have the appropriate lenght. This lenght 
            may be changed in the config options. 
        """

        s = search_string.strip()
        try:
            s = unicode(s)
        except:
            pass
        s = s.replace('*', '')

        if len(s) < self._pw.search_string_min_len:
            raise ValueError('Search string must have at least {} characters'.format(self._pw.search_string_min_len))
        if add_wildcards:
            s = u'*{0}*'.format(re.sub('[\s]+', '* *', s))
        return s

    def to_bool(self, v):
        """to bool. 


        Args:
            v (TYPE): This takes some of the commonly used bool declaratories like, True, true, v, t , y or yes and converted in to just one. Avoiding int . 

        Returns:
            TYPE: It returns a bool field. 
        """
        if isinstance(v, bool):
            return v
        if isinstance(v, unicode) or isinstance(v, str):
            return v == 'True' or v == 'true' or v == 't' or v == 'y' or v == 'yes'
        if isinstance(v, int):
            return bool(v)
        return False

    def parse_opts_searcher(self, opts, parameters):
        """parse_opts_searcher

        Args:
            opts (Args): it takes the opts saved on the search object 
            parameters (TYPE): Takes care that the opts are actually parameters available for the search. 

        Returns:
            TYPE: Description
        """
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
