import collections

from myapp.weldapp import WeldApp
from myapp.auth import make_users, User
from lxml.etree import fromstring

make_users(50)

class GridApp(WeldApp):
    model = User
    columns = [
        ('username', 'User Name'),
        ('password', 'Password'),
        ('email', 'Email Address'),
    ]

    def weld(self, pq, environ):
        data = [datum.attributes_dict for datum in self.model.objects.all()]

        pq('thead th').weld([label for _, label in self.columns])
        pq('tbody td').weld([fromstring('<span class="%s"/>' % key) for key, _ in self.columns])
        pq('tbody tr').weld(data)

def make_auth_middleware(wrap, global_conf, **app_conf):
    from repoze.who.config import make_middleware_with_config
    wrap = make_middleware_with_config(wrap, global_conf,
            app_conf['who.config_file'],
            app_conf['who.log_file'],
            app_conf['who.log_level'])
    return wrap

def make_app(global_conf, **app_conf):
    app = wrap = GridApp(global_conf, **app_conf)
    wrap = make_auth_middleware(wrap, global_conf, **app_conf)
    return wrap
