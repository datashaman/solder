from weld import weld
from pyquery import PyQuery
from myapp.fileapp import DirectoryApp

def pyquery_weld(data, config={}):
    weld(this[0], data, config)
    return this

PyQuery.fn.weld = pyquery_weld

class WeldApp(object):
    def __init__(self, global_conf, public_dir, **app_conf):
        self.public_dir = public_dir

        self.global_conf = global_conf
        self.app_conf = app_conf

        self.config = global_conf.copy()
        self.config.update(app_conf)

    def __call__(self, environ, start_response, **kwargs):
        app = DirectoryApp(self.public_dir)
        app = app(environ)

        if hasattr(app, 'content_type') and app.content_type == 'text/html':
            response = app(environ, start_response)
            if response[0]:
                pq = PyQuery(response[0])
                self.weld(pq, environ)
                response = pq.__html__()
            return response

        return app(environ, start_response)

    def weld(self, pq, environ):
        raise NotImplemented()
