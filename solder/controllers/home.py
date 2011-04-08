from solder.render import render

def index():
    return render('home', dict(title='Welcome!'))
