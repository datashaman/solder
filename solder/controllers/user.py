# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

from solder import url_for
from solder.render import template
from solder.controllers import _index, _record
from solder.models.auth import User

def filter_user(user, filter):
    result = user.attributes_dict
    result['url'] = url_for(controller='user', action='edit', username=user.username)
    result['password'] = '******'
    return result

@template('index')
def index():
    result = _index('Users', User, {}, [
            dict(name='url', display=False),
            dict(name='username', display=False),
            dict(name='email', display=False),

            dict(name='link_to', server="link_to(record['url'], record['username'])", label='Username'),
            dict(name='name'),
            dict(name='email_to', server="email_to(record['email'])", label='Email Address'),
            dict(name='password'),
        ], filter_func=filter_user, summary='Users')
    return result

@template('show')
def show(username):
    result = _record('Show User', User, dict(username=username), [
            dict(name='url', display=False),
            dict(name='email', display=False),

            dict(name='name'),
            dict(name='email_to', server="email_to(record['email'])", label='Email Address'),
            dict(name='username'),
            dict(name='password'),
        ], filter_func=filter_user)
    return result

@template('edit')
def edit(username):
    result = _record('Edit User', User, dict(username=username), [
            dict(name='url', display=False),

            dict(name='username'),
            dict(name='name'),
            dict(name='password'),
            dict(name='email'),
        ], filter_func=filter_user)
    return result
