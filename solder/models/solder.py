from redisco import models, containers

class SolderTemplate(models.Model, Audit):
    source = ''
    python = ''
    macros = {}
    paths = []

class Macro(models.Model, Audit):
    name = ''
    params = []
    decorators = []

class Decorator(models.Model, Audit):
    selector = ''
    provider = '' # Python, uses params from container macro

class Path(models.Model, Audit):
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
