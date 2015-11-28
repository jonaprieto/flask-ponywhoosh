'''

    flask_ponywhoosh extension
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Perform full-text searches over your database with Pony ORM and PonyWhoosh,
    for flask applications.

    :copyright: (c) 2015-2016 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
    :license: BSD (see LICENSE.md)

'''

from ponywhoosh import PonyWhoosh
from utils import search, full_search, delete_field

__author__ = "Jonathan S. Prieto & Ivan F. Rodriguez"
__version__ = "0.1.6c"

__all__ = ['PonyWhoosh', 'search', 'full_search', 'delete_field']
