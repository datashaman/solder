from solder.models.auth import User
users = User.objects.all()

columns = (
    ('username', 'Username'),
    ('password', 'Password'),
    ('email', 'Email Address'),
)

user = lambda username: User.objects.filter(username=username).first()

*table(objects, columns, title):
    title               is title
    #table thead th     is [label for _, label in columns]
    #table tbody td     is [fromstring('<span class="%s"/>' % key) for key, _ in columns]
    #table tbody tr     is [obj.attributes_dict for obj in objects]

*record(obj, title):
    title               is title
    #record tr          is obj.attributes_dict

/users                       is *table(users, columns, 'Users')
/user/(?P<username>.+)       is *record(user(username), 'User %s' % user(username).username)
