import faker, hashlib
from repoze.what import adapters
from redisco import models, containers
from lxml.etree import fromstring as XML
from webhelpers.html.tags import link_to

from audit import Audit

class Permission(models.Model):
    name = models.Attribute(required=True, unique=True, label='Name')
    label = models.Attribute(required=True, unique=True, label='Label')

class Group(models.Model):
    name = models.Attribute(required=True, unique=True, label='Name')
    label = models.Attribute(required=True, unique=True, label='Name')
    permissions = models.ListField(Permission, label='Permissions')

class User(models.Model):
    username = models.Attribute(required=True, unique=True, label='Username')
    password = models.Attribute(required=True, label='Password')
    email = models.Attribute(required=True, unique=True, label='Email')
    name = models.Attribute(required=True, label='Name')

    groups = models.ListField(Group, label='Groups')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.job = ['one', 'two', 'three']

    def save(self):
        if self.is_new():
            self.attributes['password'] = hashlib.md5(self.password)
        else:
            if self.password:
                self.attributes['password'] = hashlib.md5(self.password)
        return super(User, self).save()

    def validate_password(self, password):
        return self.password == hashlib.md5(password).hexdigest()

    @property
    def permissions(self):
        perms = []
        for group in self.groups:
            perms += group.permissions
        return perms

    @property
    def link(self):
        from solder import url
        return link_to(self.username, url.current(controller='user',\
            action='show', id=self.username))

    @staticmethod
    def get(username):
        return User.objects.filter(username=username).first()

class AuthPlugin(adapters.BaseSourceAdapter):
    def authenticate(self, environ, identity):
        try:
            username = identity['login']
            password = identity['password']
        except KeyError:
            return None

        authenticated = Person.objects.authenticate(username, password)
        return authenticated

    def add_metadata(self, environ, identity):
        userid = identity.get('repoze.who.userid')
        user = User.objects.find(username=userid)
        if user is not None:
            identity['user'] = user

def make_users(number):
    for user in User.objects.all():
        user.delete()

    for x in xrange(number):
        name = faker.name.name()

        user = User(username=faker.internet.user_name(name),
                password='password',
                email=faker.internet.email(name),
                name=name)
        result = user.save()
        if result is not True:
            print result
