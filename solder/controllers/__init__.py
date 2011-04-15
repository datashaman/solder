import collections, inspect
from lxml.etree import fromstring as XML
from solder import url_for

_displayed = lambda m: [c for c in m if c.get('display', True) is not False]

def callable(func):
    def _callable(self):
        value = func(self)
        if inspect.isfunction(value):
            return value(self)
        else:
            return value
    return decorator(_callable)

def _call_if_func(f, *args, **kwargs):
    return f(*args, **kwargs) if isinstance(f, collections.Callable) else f

def _index(model, filter, metadata, title, filter_func=None, caption=None, summary=None):
    cif = lambda x: _call_if_func(x, model, filter)

    displayed = _displayed(metadata)

    title = cif(title)
    rows = lambda: model.objects.filter(**filter).all()

    if filter_func is not None:
        producer = lambda: map(lambda r: filter_func(r, filter), rows())
    else:
        producer = rows

    result = dict(
        caption = cif(caption),
        summary = cif(summary),
        rows = producer,
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

def _record(model, filter, metadata, title, filter_func=None):
    record = model.objects.filter(**filter).first()

    displayed = _displayed(metadata)

    if filter_func is not None:
        record = filter_func(record, filter)

    result = dict(
        record = record,

        title = title(record) if inspect.isfunction(title) else title,
        rows = lambda: map(lambda col: dict(label=col['label'],
            value=record.get(col['name'], None)), displayed),
        welds = [
            ('title or legend', title),
        ],
        sources = [
            ('.record li', url_for(action='show', **filter)),
        ],
        metadata = metadata
    )

    return result
