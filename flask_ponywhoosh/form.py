#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: d555

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import Required


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
    add_wildcards = BooleanField('Add Wildcards', default=True)
    something = BooleanField('Something')
    submit = SubmitField('Submit')
