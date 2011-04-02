import collections, os, textwrap, sys, logging
from pprint import pprint
from routes import Mapper
from routes.middleware import RoutesMiddleware
from solder.models.auth import make_users, User
from paste.util.import_string import simple_import
from paste.httpexceptions import *

from solder.template import Template

log = logging.getLogger(__name__)

make_users(10)

def make_auth_middleware(wrap, global_conf, **app_conf):
    from repoze.who.config import make_middleware_with_config
    wrap = make_middleware_with_config(wrap, global_conf,
            app_conf['who.config_file'],
            app_conf['who.log_file'],
            app_conf['who.log_level'])
    return wrap

def route_map():
    m = Mapper()
    m.connect('/favicon.ico', controller='null')
    m.connect('/', controller='user')
    return m

class App(object):
    def __init__(self, global_conf, public_dir, **app_conf):
        self.public_dir = public_dir

        self.global_conf = global_conf
        self.app_conf = app_conf

        self.config = global_conf.copy()
        self.config.update(app_conf)

    def __call__(self, environ, start_response):
        url, routing_dict = environ['wsgiorg.routing_args']

        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)

        if environ['PATH_INFO'] == '/favicon.ico':
            return ''

        template = Template.parse('solder/controllers/user.py')

        html = 'solder/views/table.html'
        return template.render(html, environ)


def make_app(global_conf, **app_conf):
    app = wrap = App(global_conf, **app_conf)
    wrap = RoutesMiddleware(wrap, route_map())
    # wrap = make_auth_middleware(wrap, global_conf, **app_conf)
    return wrap
