import logging
from solder.render import render, template
from webhelpers.html.tags import link_to
from webhelpers.html.tools import mail_to
from decorator import decorator
from paste.debug.profile import profile_decorator

from solder.controllers import _index, _record

from solder.models.auth import make_users, User

log = logging.getLogger(__name__)

metadata = [
    dict(name='url', label='URL', display=False),

    dict(name='username', display=False),
    dict(name='link_to', label='Username'),

    dict(name='name', label='Name'),
    dict(name='password', label='Password'),

    dict(name='email', display=False),
    dict(name='email_to', label='Email Address'),
]

from solder import url_for
def filter_user(user, filter):
    user = user.attributes_dict
    user['url'] = url_for(controller='user', action='edit',
            username=user['username'])
    return user

@template('index')
def index():
    result = _index(User, {}, metadata, 'Users', filter_func=filter_user,
            summary='Users')
    return result

@template('show')
def show(username):
    return _record(User, dict(username=username), metadata,
        lambda user: 'User %s' % username, filter_func=filter_user)

@template('edit')
def edit(username):
    return _record(User, dict(username=username), metadata,
        lambda user: 'Edit User %s' % username, filter_func=filter_user)
