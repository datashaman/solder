import re, logging

from lxml.etree import fromstring
from string import Template as Tpl
from pyquery import PyQuery
from routes.base import Route
from paste.httpexceptions import *

log = logging.getLogger(__name__)


from welder import weld as w
def pyquery_weld(data, config={}):
    w(this[0], data, config)
    return this

PyQuery.fn.weld = pyquery_weld

match_error = Tpl("""
$name definition is incorrect.

Definition is: "$definition"
Must match pattern: "$pattern"
""")

class Template(object):
    source = ''
    python = ''
    macros = {}
    paths = []

    def render(self, environ):
        g = globals().copy()
        self.script = compile(self.python, '<%s:global>' % self.source, 'exec')
        exec(self.script, g)

        for path in self.paths:
            matched = path.match(environ)
            if matched:
                log.debug('Matched path %s against %s'\
                    % (path, environ['PATH_INFO']))

                with open('solder/views/%s.html' % path.view) as f:
                    source = f.read()

                pq = PyQuery(source)

                l = {}

                for key, value in matched.groupdict().items():
                    script = compile("%s = '%s'" % (key, value),\
                            '<path:%s> in %s' % (path, self.source), 'exec')
                    exec(script, g, l)

                for x, arg in enumerate(path.arguments):
                    script = compile('%s = %s' % (path.macro.parameters[x],\
                            arg), '<argument:%s> in %s' % (arg, path.macro.name), 'exec')
                    exec(script, g, l)

                for selector, provider in path.macro.decorators:
                    pq(selector).weld(eval(provider, g, l))

                return pq.__html__()
        return HTTPNotFound()

    @staticmethod
    def parse(weld):
        with open('solder/welds/%s.weld' % weld) as f:
            template = Template()
            template.source = weld

            l = f.readline()
            while not l.startswith(('*', '/')):
                template.python += l
                l = f.readline()

            while not l.startswith('/'):
                if l.strip() == '':
                    l = f.readline()
                    continue

                assert l.startswith('*'), 'Expected a macro definition, got "%s"' % l # Must be a macro

                macro = Macro()

                pattern = r'^\*(?P<name>[^\s(]+)\((?P<parameters>[^)]*)\):$'
                matched = re.match(pattern, l.strip())

                assert matched, match_error.substitute(name='Macro',\
                        pattern=pattern, definition=l.strip())

                macro.name = matched.group('name')
                template.macros[macro.name] = macro

                macro.parameters = [a.strip() for a in matched.group('parameters').split(',')]

                macro.decorators = []

                l = f.readline()

                pattern = r'^    (?P<selector>[^\s].+)\s+is\s+(?P<provider>.*)\s*$'
                matched = re.match(pattern, l)

                assert matched, match_error.substitute(name='Decorator',\
                        pattern=pattern, definition=l)

                while matched:
                    selector, provider = matched.groups(['selector',\
                        'provider'])
                    provider = compile(provider, '<provider:%s> in %s' %
                            (selector, macro.name), 'eval')
                    macro.decorators.append(matched.groups(['selector', 'provider']))

                    l = f.readline()
                    matched = re.match(pattern, l)

            while l and l != '':
                if l.strip() == '':
                    l = f.readline()
                    continue

                assert l[0] == '/' # Must be path definitions till the end of the file

                pattern =\
                r'^(?P<pattern>[^\s]*)\s+is\s+"(?P<view>\w+)"\s+with\s+(?P<macro>[^\s()]+)\((?P<arguments>.*)\)$'
                matched = re.match(pattern, l.strip())

                assert matched, match_error.substitute(name='Path',\
                        pattern=pattern, definition=l.strip())

                path = Path()
                path.pattern, path.view, macro, arguments = matched.groups(['pattern',\
                    'view', 'macro', 'arguments'])
                path.macro = template.macros[macro]
                path.arguments = [s.strip()\
                        for s in matched.group('arguments').split(',')]
                if path.arguments == ['']:
                    path.arguments = []

                template.paths.append(path)

                l = f.readline()

        return template

class Macro(object):
    name = ''
    params = []
    decorators = []

class Decorator(object):
    selector = ''
    provider = '' # Python, uses params from container macro

class Path(object):
    _pattern = ''
    macro = ''
    view = ''
    arguments = []

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
        self._re = re.compile(self._pattern)

    def match(self, environ):
        return self._re.match(environ['PATH_INFO'])

    def __repr__(self):
        return self.pattern