import os
import re


class Whoosh(object):
    """A top level class that allows to register whoosheers."""

    _underscore_re1 = re.compile(r'(.)([A-Z][a-z]+)')
    _underscore_re2 = re.compile('([a-z0-9])([A-Z])')
    whoosheers = []

    def __init__(self, app=None):

        if app:
            self.init_app(app)

    def init_app(self, app):

        self.index_path_root = app.config.get('WHOOSHEE_DIR', '') or 'whooshee'
        self.search_string_min_len = app.config.get('WHOSHEE_MIN_STRING_LEN', 3)
        self.writer_timeout = app.config.get('WHOOSHEE_WRITER_TIMEOUT', 2)
        
        # models_committed.connect(self.on_commit, sender=app)
        if not os.path.exists(self.index_path_root):
            os.makedirs(self.index_path_root)
