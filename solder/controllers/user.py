import logging, inspect, collections
from solder.render import render, template
from lxml.etree import fromstring as XML
from webhelpers.html.tags import link_to
from webhelpers.html.tools import mail_to
from decorator import decorator
from paste.debug.profile import profile_decorator

log = logging.getLogger(__name__)

def d(v):
  print v
  return v

def callable(func):
    def _callable(self):
        value = func(self)
        if inspect.isfunction(value):
            return value(self)
        else:
            return value
    return decorator(_callable)

def _format_record(record, formatters={}, filter={}):
    result = dict((k, v)
            for k, v in record.attributes_dict.items()
                if k in [col['name'] for col in metadata])

    for column, formatter in formatters.items():
        result[column] = formatter(record, filter)

    return result

def _call_if_func(f, *args, **kwargs):
    return f(*args, **kwargs) if isinstance(f, collections.Callable) else f

def _index(model, filter, metadata, title, caption=None, summary=None):
    displayed = [c for c in metadata if c.get('display', True)]
    cif = lambda x: _call_if_func(x, model, filter)
    title = cif(title)

    result = dict(
        caption = cif(caption),
        summary = cif(summary),
        rows = map(_format_record, eval(model).objects.filter(**filter).all()),
        welds = [
            ('title or h1', title),
            ('thead th', [c['label'] for c in displayed]),
            ('tbody td', [XML('<span class="%s"/>' % c['name']) for c in displayed]),
        ],
        sources = [
            ('tbody tr', url_for(controller='user', action='index')),
        ],
        metadata = metadata
    )

    return result

def _record(model, filter, metadata, title):
    first = eval(model).objects.filter(**filter).first()

    result = dict(
        record = _format_record(first, filter),

        title = title(first) if inspect.isfunction(title) else title,
        rows = [dict(label=col['label'], value=record[col['name']])\
                for col in metadata],
        welds = [
            ('title or legend', title),
        ],
        sources = [
            ('.record li', url_for(action='show', **filter)),
        ],
        metadata = metadata
    )
    return result

from solder.models.auth import make_users, User

# make_users(30)

from solder import url_for

metadata = [
    dict(name='username', label='Username'),
    dict(name='name', label='Name'),
    dict(name='password', label='Password'),
    dict(name='url', label='URL', display=False),
    dict(name='email', label='Email Address', display=False),
]

url = lambda u: url_for(controller='user', action='edit', username=u.username)

formatters = dict(
    url=lambda u, f: url(u),
    password=lambda u, f: '******',
)

@template('index')
def index():
    result = _index('User', {}, metadata, 'Users', 'Users')
    return result

@template('show')
def show(username):
    return _record(('User', dict(username=username)), metadata,\
        lambda user: 'User %s' % username)

@template('edit')
def edit(username):
    return _record(('User', dict(username=username)), metadata,\
        lambda user: 'Edit User %s' % username)
