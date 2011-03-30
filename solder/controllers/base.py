class BaseController(object):
    template = None

    def __call__(self, environ):
        with open(self.template) as template:
            self.pq = PyQuery(template.read())

        self.environ = environ
        self.weld()

        return self.pq.__html__()

    def weld(self):
        raise NotImplemented()

    def __setitem__(self, name, value):
        self.pq(name).weld(value)
