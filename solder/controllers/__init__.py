import collections, inspect, logging
from pyquery import PyQuery
from lxml.etree import fromstring as XML
import solder
from redisco.models.base import ModelBase
from nose.tools import *

log = logging.getLogger(__name__)
_d = lambda f, *a, **k: f(*a, **k) # log.debug('%s %s %s' % (f, a, k)) and f(*a, **k)

_imeta = lambda m: dict((c['name'], c) for c in m)
_displayed = lambda m: [c['name'] for c in m if c.get('display', True) is not False]

_server_scripts = lambda m: dict((c['name'], c['server']) for c in m if 'server' in c)
_client_scripts = lambda m: dict((c['name'], c['client']) for c in m if 'client' in c)

def _isa(model, klass):
    ok_(isinstance(model, klass), '%s is not a %s' % (model.__class__.__name__, klass.__name__))

def _label(model, col):
    _isa (model, ModelBase)
    _isa (col, dict)

    label = col.get('label', None)
    if label is None and col['name'] in model._attributes.keys():
        label = model[col['name']].label
    if label is None:
        label = col['name'].capitalize()
    return label

def _apply_scripts(scripts, records):
    _isa (scripts, dict)
    ok_ (inspect.isfunction(records), '%s is not a function' % records)

    def link_to(href, text):
        return '<a href="%s">%s</a>' % (href, text)

    def email_to(email, text=None):
        if text is None:
            text = email
        return link_to('mailto:%s' % email, text)

    records = records()
    for record in records:
        for column, script in scripts.items():
            record[column] = eval(script)
    return records

def _apply_filter_func(filters, filter_func, records):
    return records if filter_func is None else lambda: map(lambda r: filter_func(r, filters), records)

def _records(model, filters, metadata, filter_func=None, page=1, page_size=10,
        **result):
    start = (page - 1) * page_size
    end = start + page_size - 1

    server_scripts = _server_scripts(metadata)

    records = lambda: _apply_scripts(server_scripts,
            _apply_filter_func(filters, filter_func,
            model.objects.filter(**filters)[start:end]))

    def assign_label(c):
        c['label'] = _label(model, c)
        return c

    metadata = map(assign_label, metadata)

    result.update(dict(
        model = model.__name__,
        filters = filters,
        start = start,
        end = end,
        records = records,
        metadata = _imeta(metadata),
        displayed = _displayed(metadata),
        scripts = _client_scripts(metadata),
    ))
    return result

def _index(title, model, filters, metadata, filter_func=None, *args, **kwargs):
    result =_records(model, filters, metadata, filter_func, *args, **kwargs)
    result.update(dict(
        welds = [
            ('title or h1', title),
            ('thead th', [result['metadata'][c]['label'] for c in result['displayed']]),
            ('tbody td', [XML('<span class="%s"/>' % c) for c in\
                result['displayed']]),
        ],
        sources = [
            ('tbody tr', solder.url_for(action='index')),
        ],
    ))

    return result

def _record(title, model, filters, metadata, filter_func=None, *args, **kwargs):
    result =_records(model, filters, metadata, filter_func, *args, **kwargs)
    result.update(dict(
        welds = [
            ('title or legend', title),
            ('.record li', [dict(label=result['metadata'][c]['label'],
                value=result['records']()[0].get(c, '')) for c in
                result['displayed']]),
        ],
    ))
    return result
