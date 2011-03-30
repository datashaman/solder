from solder.models.auth import User
objects = User.objects.all()

columns = [
    ('username', 'User Name'),
    ('password', 'Password'),
    ('email', 'Email Address'),
]

table:/users
  #table thead th         < [label for _, label in columns]
  #table tbody td         < [fromstring('<span class="%s"/>' % key) for key, _ in columns]
  #table tbody tr         < [obj.attributes_dict for obj in objects]
