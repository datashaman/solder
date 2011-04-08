import simplejson as json
from lxml.etree import tostring
from pyquery import PyQuery

from welder import weld as w

def pyquery_weld(data, config={}):
    if len(this):
        w(this[0], data, config)
    return this

PyQuery.fn.weld = pyquery_weld

class template(object):
    def __init__(self, name, layout='layout'):
        self.name = name
        self.layout = layout

    def __call__(self, func, *args, **kwargs):
        def _func(*args, **kwargs):
            data = func(*args, **kwargs)
            data.update(dict(
                _template=self.name,
                _weld=True,
                _layout=self.layout,
            ))
            return data
        return _func

def render(template, data, weld=True, layout='layout'):
    with open('./solder/templates/%s.html' % template) as f:
        t = PyQuery(f.read())

    t_body = t('body')

    if weld:
        if 'welds' in data:
            welds = data['welds']

            if len(welds):
                for weld in welds:
                    t(weld[0]).weld(weld[1])

        if 'sources' in data:
            sources = data['sources']

            script = t('<script id="welds" type="text/javascript"></script>')
            text = """
            require(["jquery", '/scripts/solder.js'], function($) {
                $(function() {
            """

            if 'scripts' in data:
                text += """
                    function solder(p, e, k, v) {
                """

                for name, scr in data['scripts'].items():
                    text += """
                        if(k=='%s') return %s;
                    """ % (name, scr)

                text += """
                        return v;
                    }
                """

                map_func = ', solder'
            else:
                map_func = ''

            for source in sources:
                text += "$('%s').solder('%s'" % source + map_func + ");"

            text += """
                });
            });
            """
            script.text(text)
            t_body.append(script)

    if layout is not None:
        with open('./solder/templates/%s.html' % layout) as f:
            l = PyQuery(f.read())

        l('head').append(t('head *'))
        l_body = l('body')

        for name, value in t_body[0].items():
            if name == 'class':
                l_body.addClass(value)
            else:
                l_body.attr(name, value)

        html = t_body.html()
        if html:
            l('#content').html(html)

        t = l

    return t.__html__()
