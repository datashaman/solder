import re, logging, inspect

from string import Template
from pyquery import PyQuery
from routes.mapper import Mapper

import collections, os, textwrap, sys, logging, logging.config
import simplejson as json
from webob import Request, Response
from paste.util.import_string import simple_import
from paste.httpexceptions import *
from paste.deploy.converters import asbool

request = None
cache = None
log = None
url = None
app = None

from routes.util import url_for

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
        self.debug = debug

        super(Solder, self).__init__(directory='./solder/controllers',
                always_scan=debug, explicit=False)

        self.minimization = True
        self.connect_routes()

    def _create_response(self):
        res = Response(status=200,\
            content_type='text/html')
        return res

    def _create_content(self, action, urlvars, is_xhr):
        content = action(**urlvars)

        res = self._create_response()

        if is_xhr:
            if isinstance(content, dict) and 'welds' in content:
                del content['welds']
            data = content.copy()
            for name, value in data.items():
                while inspect.isfunction(value):
                    value = value()
                data[name] = value
            res.body = json.dumps(data)
            res.content_type = 'application/json'
        elif isinstance(content, dict) and '_template' in content:
            res.body = render.render(content['_template'], content,
                    content['_weld'], content['_layout'])

        return res

    def _create_not_found(self):
        res = self._create_response()
        res.status = 404
        res.body = 'Page not found'
        return res

    def __call__(self, environ, start_response):
        global cache, request

        cache = environ['beaker.cache']

        app_cache = cache.get_cache(__name__)

        request = Request(environ)

        urlvars = request.urlvars.copy()
        if 'controller' in urlvars and 'action' in urlvars:
            if urlvars['action'].startswith('_'):
                start_response(status, headers)
                return HTTPNotFound()

            module_reference = 'solder.controllers.%s' % urlvars['controller']
            module = simple_import(module_reference)

            action = getattr(module, urlvars['action'])

            if inspect.isfunction(action):
                cache_key = urlvars.copy()

                del urlvars['controller']
                del urlvars['action']

                cache_key['hash'] = str(urlvars)
                cache_key['is_xhr'] = request.is_xhr

                # TODO something with format
                if 'format' in urlvars:
                    del urlvars['format']

                key = Template('$controller-$action-$hash-$is_xhr')
                key = key.substitute(**cache_key)

                res = app_cache.get(key=key,
                        createfunc=lambda: self._create_content(action,\
                            urlvars, request.is_xhr))
            else:
                res = app_cache.get(key='not-found', createfunc=self._create_not_found)
        else:
            res = app_cache.get(key='not-found', createfunc=self._create_not_found)

        return res(environ, start_response)

    def connect_routes(self):
        self.collection('users', 'user', member_prefix='/{username}', formatted=False)
        self.connect('home', '', controller='home')

def make_auth_middleware(wrap, global_conf, **app_conf):
    from repoze.who.config import make_middleware_with_config
    wrap = make_middleware_with_config(wrap, global_conf,
            app_conf['who.config_file'],
            app_conf['who.log_file'],
            app_conf['who.log_level'])
    return wrap

def make_app(global_conf, **app_conf):
    global app, log

    logging.config.fileConfig(global_conf['__file__'])
    log = logging.getLogger('solder')

    import solder.logger

    app = wrap = Solder(global_conf, **app_conf)

    from beaker.middleware import SessionMiddleware
    wrap = SessionMiddleware(wrap, app.config)

    from beaker.middleware import CacheMiddleware
    wrap = CacheMiddleware(wrap, app.config)

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

    from weberror.evalexception import make_general_exception
    wrap = make_general_exception(wrap, global_conf,
            asbool(app.config['interactive']))

    from paste.fileapp import DirectoryApp
    public = DirectoryApp('./solder/public')

    from paste.cascade import Cascade
    wrap = Cascade([public, wrap], [403, 404])

    return wrap
