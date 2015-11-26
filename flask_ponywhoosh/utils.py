#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: d555

from pony import orm

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
    return model._pw_index_.search(*arg, **kw)


@orm.db_session
def delete_field(model, *arg):
    """Delete_field 

    Args:
        model (TYPE): Is the model from where you want to delete an specific field. 
        *arg: Fiedls. 

    Returns:
        TYPE: model without the desired field. 
    """
    return model._pw_index_.delete_field(*arg)


def full_search(pw, *arg, **kw):
    """ This function search in every model registered. And portrays the result in a dictionary where the keys are the models. 

    Args:
        pw (PonyWhoosh): This is where all the indexes are stored. 
        *arg: The search string. 
        **kw: The options available for a single search wildcards, something, fields, models, etc. 

    Returns:
        TYPE: Dictionary with all the the results for the models. 
    """
    return pw.search(*arg, **kw)
