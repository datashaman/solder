import collections, os, textwrap, re, sys
from pyquery import PyQuery
from lxml.etree import fromstring
from routes import Mapper
from routes.middleware import RoutesMiddleware
from solder.models.auth import make_users, User
from paste.util.import_string import simple_import
from paste.httpexceptions import *

import welder
def pyquery_weld(data, config={}):
    welder.weld(this[0], data, config)
    return this

PyQuery.fn.weld = pyquery_weld

# make_users(10)

def make_auth_middleware(wrap, global_conf, **app_conf):
    from repoze.who.config import make_middleware_with_config
    wrap = make_middleware_with_config(wrap, global_conf,
            app_conf['who.config_file'],
            app_conf['who.log_file'],
            app_conf['who.log_level'])
    return wrap

def route_map():
    m = Mapper()
    m.collection('users', 'user', 'user')
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
        if 'controller' in routing_dict:
            source = 'solder/controllers/%s.py' % routing_dict['controller']
            template = 'solder/views/table.html'

            result = weld(template, source)

            status = '200 OK'
            headers = [('Content-Type', 'text/html')]
            start_response(status, headers)

            return result
        else:
            response = HTTPNotFound()

        return response(environ, start_response)

def weld(template_file, source_file):
    with open(template_file) as f:
        pq = PyQuery(f.read())

    template_basename = os.path.basename(template_file).split('.')[-2]

    glob = globals()
    local = locals()

    with open(source_file) as f:
        routes = {}
        preamble = ''
        pattern = None
        route = None
        selector = None
        match = False
        first = True

        for l in f.readlines():
            re_match = re.search(r'(.+):(.+)', l.strip())

            if re_match:
                template = re_match.group(1)
                pattern = re_match.group(2)

                match = template_basename == template

                route = routes[pattern] = {}

                if first:
                    script = compile(preamble, '<preamble:%s>' % source_file, 'exec')
                    exec(preamble, glob, local)
                    first = False
            else:
                if route is None:
                    preamble += l
                elif l.startswith('  ') and match:
                    m = re.search('(.*)\s+\<\s+(.*)', l.strip())
                    if m:
                        selector = m.group(1).strip()
                        provider = m.group(2).strip()

                        routes[pattern][selector] = provider

                        script = compile(provider, '<selector:%s>' % selector, 'eval')
                        data = eval(script, glob, local)

                        pq(selector).weld(data)
    return pq.__html__()

def make_app(global_conf, **app_conf):
    app = wrap = App(global_conf, **app_conf)
    wrap = RoutesMiddleware(wrap, route_map())
    wrap = make_auth_middleware(wrap, global_conf, **app_conf)
    return wrap
