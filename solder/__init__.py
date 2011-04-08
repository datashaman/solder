import re, logging, inspect

from string import Template
from pyquery import PyQuery
from routes.mapper import Mapper

import collections, os, textwrap, sys, logging
import simplejson as json
from webob import Request, Response
from paste.util.import_string import simple_import
from paste.httpexceptions import *
from paste.deploy.converters import asbool

from beaker.cache import CacheManager

cache = CacheManager(type='redis', url='localhost:6379', lock_dir='./data')
log = logging.getLogger(__name__)
url = None
app = None

from routes.util import url_for

def make_auth_middleware(wrap, global_conf, **app_conf):
    from repoze.who.config import make_middleware_with_config
    wrap = make_middleware_with_config(wrap, global_conf,
            app_conf['who.config_file'],
            app_conf['who.log_file'],
            app_conf['who.log_level'])
    return wrap

class Solder(Mapper):
    source = ''
    python = ''
    macros = {}
    paths = []

    request = None

    def __init__(self, global_conf, **app_conf):
        self.global_conf = global_conf
        self.app_conf = app_conf

        self.config = global_conf.copy()
        self.config.update(app_conf)

        debug = asbool(self.config['debug'])
        super(Solder, self).__init__(directory='./solder/controllers',
                always_scan=debug, explicit=False)

        self.debug = debug
        self.minimization = True
        self.connect_routes()

    def __call__(self, environ, start_response):
        req = Request(environ)
        res = Response(request=req, environ=environ, status=200,\
            content_type='text/html')

        urlvars = req.urlvars.copy()
        if 'controller' in urlvars and 'action' in urlvars:
            if urlvars['action'].startswith('_'):
                start_response(status, headers)
                return HTTPNotFound()

            module_reference = 'solder.controllers.%s' % urlvars['controller']
            module = simple_import(module_reference)

            action = getattr(module, urlvars['action'])

            if inspect.isfunction(action):
                del urlvars['controller']
                del urlvars['action']

                # TODO something with format
                if 'format' in urlvars:
                    del urlvars['format']

                content = action(**urlvars)

                if req.is_xhr:
                    if isinstance(content, dict) and 'welds' in content:
                        del content['welds']
                    res.body = json.dumps(content)
                    res.content_type = 'application/json'
                elif isinstance(content, dict) and '_template' in content:
                    res.body = render.render(content['_template'], content,
                            content['_weld'], content['_layout'])
            else:
                res.status = 404
                res.body = 'Page not found'
        else:
            res.status = 404
            res.body = 'Page not found'

        return res(environ, start_response)

    def connect_routes(self):
        self.collection('users', 'user', member_prefix='/{username}', formatted=False)
        self.connect('home', '', controller='home')

def make_app(global_conf, **app_conf):
    global app

    app = wrap = Solder(global_conf, **app_conf)

    from routes.middleware import RoutesMiddleware
    wrap = RoutesMiddleware(wrap, app)

    if False and app.debug:
        from repoze.profile.profiler import AccumulatingProfileMiddleware
        wrap = AccumulatingProfileMiddleware(
                wrap,
                log_filename='./logs/profile.log',
                discard_first_request=True,
                flush_at_shutdown=True,
                path='/_profile_'
        )

    from paste.fileapp import DirectoryApp
    public = DirectoryApp('./solder/public')

    from paste.cascade import Cascade
    wrap = Cascade([public, wrap], [403, 404])

    return wrap
