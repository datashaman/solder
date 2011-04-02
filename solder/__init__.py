import collections, os, textwrap, sys, logging
from paste.util.import_string import simple_import
from paste.httpexceptions import *

from solder.template import Template

log = logging.getLogger(__name__)

from solder.models.auth import make_users
make_users(10)

def make_auth_middleware(wrap, global_conf, **app_conf):
    from repoze.who.config import make_middleware_with_config
    wrap = make_middleware_with_config(wrap, global_conf,
            app_conf['who.config_file'],
            app_conf['who.log_file'],
            app_conf['who.log_level'])
    return wrap

class App(object):
    def __init__(self, global_conf, public_dir, **app_conf):
        self.public_dir = public_dir

        self.global_conf = global_conf
        self.app_conf = app_conf

        self.config = global_conf.copy()
        self.config.update(app_conf)

    def __call__(self, environ, start_response):
        template = Template.parse('user')

        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)

        return template.render(environ)

def make_app(global_conf, **app_conf):
    app = wrap = App(global_conf, **app_conf)
    return wrap
