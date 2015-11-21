'''

flask_ponywhoosh extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adds capabilities to perform full-text search over your modules of Pony ORM
for flask applications. Enjoy it!

:copyright: (c) 2015 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
:license: BSD (see LICENSE.md)

Attributes:
    basedir (TYPE): Description
'''

from collections import defaultdict
from datetime import datetime
import os
from pprint import pprint
import re
import sys

from __version__ import __version__
from flask import render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask.views import View
import jinja2
from pony import orm
from whoosh import fields, index, qparser
import whoosh
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import Required


basedir = os.path.abspath(os.path.dirname(__file__))


class SearchForm(Form):
    """This is the searching form that we will be use to make our search engine website.
    
    Attributes:
        except_field (StringField): Fields you do not want to include in the search results.
        fields (StringField): Fields, separated by comma,  where you want to search. 
        models (StringField): Models, separated by comma, where you want to search. 
        query (StringField): What you want to search. 
        something (BooleanField): Option to literal search first, but in case there are no results available, it performs a search with wild_cards. 
        submit (SubmitField): Button to submit the form. 
        wildcards (BooleanField): Checkbox 
    """
    query = StringField('What are you looking for?')
    models = StringField('Models')
    fields = StringField('Fields')
    except_field = StringField('Except in Fields')
    wildcards = BooleanField('Add Wildcards')
    something = BooleanField('Something')
    submit = SubmitField('Submit')


class IndexView(View):
    """This is all the setting for the template index.html in the templates folder. 
        
        methods (list): POST and GET 
        wh (whoosheers): The whoosheers is the object where all the whoosheer are saved. 
    """
    methods = ['POST', 'GET']

    def __init__(self, wh):
        """__init__
        
        Args:
            wh (whoosheers): Initializes the Index view for the /ponywhoosh.
        """
        self.wh = wh
        self.DEBUG = self.wh.DEBUG

    def dispatch_request(self):
        """ This form is plugeable. That means that all what you need to do is to install the package and run
        the url :: /ponywhoosh (You may change it in the config) and get the results.
        
        Returns:
            Results: The results are sent to the template using bootstrap. 
            They are renderized using whether a grid or a table, depending on what 
            models did you register. By default the first field registered is considered
            the one that will be contained in the tittle of each searh result.
        """
        ctx = {'form': SearchForm()}
        query, fields = None, None
        wildcards = True
        except_field = None
        # sortedby= None
        form = SearchForm()
        if self.DEBUG:
            print 'form:'
            pprint(form.data)

        if form.validate_on_submit():
            
            query = form.query.data
            models = re.split('\W+', form.models.data, flags=re.UNICODE)
            fields = re.split('\W+', form.fields.data, flags=re.UNICODE)
            except_fields = re.split(
                '\W+', form.except_field.data, flags=re.UNICODE)
            wildcards = form.wildcards.data
            something = form.something.data

            results = self.wh.search(
                query,
                add_wildcards=wildcards,
                something=something,
                include_entity=True,
                fields=fields,
                models=models,
                except_fields=except_fields,
                use_dict=False
            )

            if self.DEBUG:
                print 'form = ',
                pprint({
                    'query': query,
                    'add_wildcards': wildcards,
                    'something': something,
                    'include_entity': True,
                    'fields': fields,
                    'models': models,
                    'except_fields': except_fields
                })

                print "results = "
                pprint(results)

            return render_template(
                'ponywhoosh/results.html',
                entidades=list(self.wh.entities.keys()),
                form=form,
                results=results,
                n=results['cant_results'],
                labels=results['results'].keys()
            )

        return render_template(
            'ponywhoosh/index.html',
            form=form,
            query=query
        )


class Whoosheer(object):
    """A top lev....
    
    Attributes:
        DEBUG (bool): Activates debugin. 
        parameters (dict): Is a dictionary that contains parameters to manage the whoosheer object.
        * limit: 
        *  Optimize: This option indexes all the documents again to improve search runtime. However 
        having the index optimizing everytime a new document is added may cause to register documents way too slow. 
        * reverse= This option changes de order in which the documents are shown in the search results object.
        *  scored: This option adds a boost in the column, giving it more importance when searching is performed. 
        *  sortedby: This option let you decide the order based in a specific column. For example, price, age, etc.

    """
    parameters = {
        'limit': 0,
        'optimize': False,
        'reverse': False,
        'scored': u'',
        'sortedby': u'',
    }

    def __init__(self, wh):
        """Summary
        
        Args:
            wh (Whoosh): Initializes de whoosheer. 
        """
        self.wh = wh
        self.DEBUG = wh.DEBUG

    def add_field(self, fieldname, fieldspec=fields.TEXT):
        """Add Field
        
        Args:
            fieldname (Text): This parameters register a new field in specified model.
            fieldspec (Name, optional): This option adds various options as were described before. 
        
        Returns:
            TYPE: The new schema after deleted is returned. 
        """
        self.index.add_field(fieldname, fieldspec)
        return self.index.schema

    def delete_field(self, field_name):
        """This function deletes one determined field using the command MODEL.wh.delete_field(FIELD)
        
        Args:
            field_name (string): This argument let you delete some field for some model registered in the whoosheer. 
        
        Returns:
            INDEX: The new schema after deleted is returned. 
        """
        self.index.remove_field(field_name.strip())
        return self.index.schema

    def delete_documents(self):
        """
        Deletes all the  documents using the  pk associated to them. 
        
        Returns:
            The new index with the document deleted. 
        """
        pk = unicode(self.primary)
        for doc in self.index.searcher().documents():
            if pk in doc:
                doc_pk = unicode(doc[pk])
                self.index.delete_by_term(pk, doc_pk)

    def optimize(self):
        """ The index is reindexed, optimizing the run time of searchings and space used. Everytime a document is added a new file would be created, but optimizing would reduce all to just one. 
        
        
        Returns:
            TYPE: Index optimized. 
        """
        self.index.optimize()

    def counts(self):
        """This method counts all the documents contained in  a certain registered model. 
        
        Returns:
            Int: A number with all the documents a model have. 
        """
        return self.index.doc_count()

    @orm.db_session
    def charge_documents(self):
        """
        This method allow you to charge documents you already have 
            in your database. In this way an Index would be created according to 
            the model and fields registered. 
        
        Returns:
            An index updated with new documents.  
        """
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
            **opt: The following opts are available for the search function: 
            * add_wildcars(bool): This opt allows you to search no literal queries. 
            * fields: This opt let you filter your search result on some model by the fields you want to search.
            * include_entity: This opt let you see not only the result and the register fields but all the instance from the entity of the database. 
            * except_fields: Tell the searcher to not look on these fields. 
            * use_dict: This option let you activate the dict for the items in the search result, or just view them as a list. 
            We implement this because we wanted that the  first field registered of the model would be the most important one. 
            As was explained in the IndexView section. 
        Returns:
            TYPE: Description
        """
        if self.DEBUG:
            print 'VERSION -> ', __version__
            print 'opt:'
            pprint(opt)

        prepped_string = self.prep_search_string(
            search_string, self.to_bool(opt.get('add_wildcards', False)))

        with self.index.searcher() as searcher:

            fields = opt.get('fields', self.schema.names())
            fields = filter(lambda x: len(x) > 0, fields)

            field = opt.get('field', '')
            if len(field) > 0:
                if isinstance(field, str) or isinstance(field, unicode):
                    fields = [field]
                elif isinstance(field, list):
                    fields = fields + field

            fields = filter(lambda x: len(x) > 0, fields)

            if self.DEBUG:
                print 'FIELDS #1 -> ', fields

            if len(fields) == 0:
                fields = self.schema.names()

            if len(fields) > 0:
                fields = set(fields) & set(self.schema.names())
                fields = list(fields)

            if self.DEBUG:
                print 'FIELDS #2 -> ', fields

            except_fields = opt.get('except_fields', [])
            except_fields = filter(lambda x: len(x) > 0, except_fields)

            if len(except_fields) > 0:
                fields = list(set(fields) - set(except_fields))

            if self.DEBUG:
                print 'FIELDS #3 -> ', fields

            parser = whoosh.qparser.MultifieldParser(
                fields, self.index.schema,
                group=opt.get('group', qparser.OrGroup))

            query = parser.parse(prepped_string)
            search_opts = self.parse_opts_searcher(opt, self.parameters)
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
                    dic_entity = entity.to_dict()
                    if opt.get('use_dict', True):
                        ans['entity'] = dic_entity
                    else:
                        fields_missing = set(dic_entity.keys()) - set(self.index_fields)
                        ans['other_fields'] = [(k, dic_entity[k]) for k in fields_missing]
                        ans['entity'] = [ (k, dic_entity[k]) for k in self.index_fields ]
                    ans['model'] = self.index_subdir

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

        if self.DEBUG:
            print 'SEARCH_STRING_MIN_LEN -> ', self.wh.search_string_min_len

        if len(s) < self.wh.search_string_min_len:
            raise ValueError('Search string must have at least {} characters'.format(
                self.wh.search_string_min_len))
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


class Whoosh(object):

    """A top level class that allows to register whoosheers.
    
    Attributes:
        #.DEBUG (bool): Description
        #.entities (dict): This is a dictionary to store entities from db.
        #.index_path_root (str): this is the name where the folder of the whoosheers are going to be stored.
        #.route (TYPE): This config let you set the route for the url to run the html template.
        #.search_string_min_len (int): This item let you config the minimun string value possible to perform search. 
        #.template_path (TYPE): Is the path where the folder of templates will be store. 
        #.writer_timeout (int): Is the time when the writer should stop the searching. 
    """

    _whoosheers = {}
    index_path_root = 'whooshee'
    writer_timeout = 2
    entities = {}
    search_string_min_len = 2
    DEBUG = False

    def __init__(self, app=None):
        """Summary
        
        Args:
            app (TYPE, optional): Description
        """
        if app is not None:
            self.init_app(app)

        if not os.path.exists(self.index_path_root):
            os.makedirs(self.index_path_root)

    def init_app(self, app):
        """Initializes the App. 
        
        Args:
            app (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        self.DEBUG = app.config.get('PONYWHOOSH_DEBUG', False)
        self.index_path_root = app.config.get('WHOOSHEE_DIR',  'whooshee')
        self.search_string_min_len = app.config.get(
            'WHOSHEE_MIN_STRING_LEN', 3)
        self.writer_timeout = app.config.get('WHOOSHEE_WRITER_TIMEOUT', 2)
        self.route = app.config.get('WHOOSHEE_URL', '/ponywhoosh/')
        self.template_path = app.config.get('WHOOSHEE_TEMPLATE_PATH',
                                            os.path.join(basedir, 'templates')
                                            )
        if self.DEBUG:
            print 'PONYWHOOSH_DEBUG -> ', self.DEBUG
            print 'WHOOSHEE_DIR  -> ', self.index_path_root
            print 'WHOOSHEE_MIN_STRING_LEN  -> ', self.search_string_min_len
            print 'WHOOSHEE_WRITER_TIMEOUT -> ', self.writer_timeout
            print 'WHOOSHEE_TEMPLATE_PATH -> ', self.template_path
            print 'WHOOSHEE_URL -> ',  self.route

        loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader(self.template_path)
        ])

        app.jinja_loader = loader
        app.add_url_rule(
            self.route,
            view_func=IndexView.as_view(
                'ponywhoosh', wh=self)
        )

    def delete_whoosheers(self):
        """This set to empty all the whosheers registered. 
        
        Returns:
            TYPE: This empty all the whoosheers. 
        """
        self._whoosheers = {}

    def whoosheers(self):
        """Summary
        
        Returns:
            TYPE: This returns all the whoosheers items stored. 
        """
        return [v for k, v in self._whoosheers.items()]

    def create_index(self, wh):
        """Creates and opens index for given whoosheer.
        
        If the index already exists, it just opens it, otherwise it creates it first.
        
        Args:
            wh (TYPE): All the whoosheers stored.
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
        """
        Registers a given whoosheer:
        
        * Creates and opens an index for it (if it doesn't exist yet)
        * Sets some default values on it (unless they're already set)
        * Replaces query class of every whoosheer's model by WhoosheeQuery
        
        Args:
            wh (TYPE): Description
        """
        if not hasattr(wh, 'index_subdir'):
            wh.index_subdir = wh.__name__

        self._whoosheers[wh.index_subdir] = wh
        self.create_index(wh)
        return wh

    def register_model(self, *index_fields, **kw):
        """Registers a single model for fulltext search. This basically creates
        a simple Whoosheer for the model and calls self.register_whoosheer on it.
        
        Args:
            *index_fields: all the fields indexed from the model. 
            **kw: The options for each field, sortedby, stored... 
        """

        mwh = Whoosheer(wh=self)
        mwh.kw = kw
        mwh.index_fields  = index_fields

        def inner(model):
            """This look for the types of each field registered in the whoosher, whether if it is 
            Numeric, datetime or Boolean. 
            
            Args:
                model (TYPE): Description
            
            Returns:
                TYPE: Description
            """
            mwh.index_subdir = model._table_
            if not mwh.index_subdir:
                mwh.index_subdir = model.__name__

            self.entities[mwh.index_subdir] = model

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
                        elif field.py_type.__name__ == 'bool':
                            mwh.schema_attrs[
                                field.name] = whoosh.fields.BOOLEAN(stored=True)
                        lista[field.name] = field.py_type.__name__
                    else:

                        mwh.schema_attrs[field.name] = whoosh.fields.TEXT(**kw)

            mwh.schema = whoosh.fields.Schema(**mwh.schema_attrs)
            self.register_whoosheer(mwh)

            def _middle_save_(obj, status):
                """Summary
                
                Args:
                    obj (TYPE): Description
                    status (TYPE): Description
                
                Returns:
                    TYPE: Description
                """
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
        whoosheers = self.whoosheers()

        models = kw.get('models', self.entities.values())
        models = [self.entities.get(model, None) if isinstance(model, str) or isinstance(model, unicode)
                  else model for model in models]
        models = filter(lambda x: x is not None, models)

        if models == [] or not models:
            models = self.entities.values()

        if self.DEBUG:
            print "SEARCHING ON MODELS -> ", models

        whoosheers = [m._wh_ for m in models if hasattr(m, '_wh_')]

        if whoosheers == []:
            return output

        runtime, cant = 0, 0

        ma = defaultdict(set)
        for whoosher in whoosheers:
            res = whoosher.search(*arg, **kw)
            runtime += res['runtime']
            cant += res['cant_results']

            output['results'][whoosher.index_subdir] = {
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


@orm.db_session
def search(model, *arg, **kw):
    """Summary
    
    Args:
        model (TYPE): Description
        *arg: Description
        **kw: Description
    
    Returns:
        TYPE: Description
    """
    return model._wh_.search(*arg, **kw)


@orm.db_session
def delete_field(model, *arg):
    """Delete_field 
    
    Args:
        model (TYPE): Is the model from where you want to delete an specific field. 
        *arg: Fiedls. 
    
    Returns:
        TYPE: model without the desired field. 
    """
    return model._wh_.delete_field(*arg)


def full_search(wh, *arg, **kw):
    """ This function search in every model registered. And portrays the result in a dictionary where the keys are the models. 
    
    Args:
        wh (Whoosheer): This is where all the whoosheers are stored. 
        *arg: The search string. 
        **kw: The options available for a single search wildcards, something, fields, models, etc. 
    
    Returns:
        TYPE: Dictionary with all the the results for the models. 
    """
    return wh.search(*arg, **kw)
