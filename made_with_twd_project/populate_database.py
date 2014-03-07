import os

def populate():
    itech= add_cat('iTECH')
    dim = add_cat('DIM3')

    milad = add_rater('milad','test','Milad','Jones','milad@jones.com')
    fergus = add_rater('fergus','test','Fergus','Smyth','fergus@smyth.com')
    doug = add_rater('doug','test','Doug','McTaggert','doug@taggert.com')

    ateam = add_team('alpha','test','Adam','Smith','', 'AlphaNoobs','Adam, Bob, Charlie')
    bteam = add_team('beta','test','Danny','DeVito', '','BetaMaxs','Danny, Eddy, Freddy')
    gteam = add_team('gamma','test','Geri','Halliway', '','GammaPros','Geri, Heido, Ingrid')

    pf  = add_demo(ateam, dim, 'PageFetch','Test your web searching skills', 'A game designed to test and improve your web searching abilities.',2014, 'http://pagefetch.pythonanywhere.com')
    asg = add_demo(bteam, dim, 'ASG','Test your search skills', 'A game designed to test your searching abilities.',2014, 'http://www.iretrieve.info')
    rm  = add_demo(gteam, itech, 'RetrieveMe','Test your site searching skills', 'A game designed to test how good you are at finding information on Glasgow Unis website',2014, 'http://www.retrieveme.info')


    add_rating(milad, pf, 'It was really good!', 4)
    add_rating(milad, asg, 'Really abstract - not sure I follow what is happening', 2)
    add_rating(milad, rm, 'Works great - but the gameplay was too easy', 4)
    add_rating(fergus, asg, 'Odd. Seriously Odd. I do not get it.', 1)
    add_rating(doug, rm, 'Lots of fun to play - slick and easy to use.', 5)


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c


def add_user(un, pw, fname, sname, email):
    u = User.objects.get_or_create(username=un, first_name=fname, last_name=sname, email=email)[0]
    u.set_password(pw)
    u.save()

    return u

def add_rater(un, pw, fname, sname, email):

    u = add_user(un, pw, fname, sname, email)
    r = Rater.objects.get_or_create(user=u, active=True)[0]
    return r

def add_team(un, pw, fname, sname, email, team_name, members):

    #frist create user in user db
    u = add_user(un, pw, fname, sname, email)
    # then create team with ref to user
    t = Team.objects.get_or_create(user=u, name=team_name, members=members)[0]
    return t

def add_demo(team, cat, name, tagline, description, year, url):
    d = Demo.objects.get_or_create(team=team, category=cat, name=name, tagline=tagline, description=description, year=year, url=url,live=True)[0]
    return d

def add_rating(rater, demo, comment, score):
    r = Rating.objects.get_or_create(rater=rater, demo=demo, comment=comment, score=score)
    demo.rating_count = demo.rating_count + 1
    demo.rating_sum = demo.rating_sum + score
    demo.save()
    return r


if __name__ == '__main__':
    print "Starting ShowCase population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'made_with_twd_project.settings')
    from showcase.models import Category, Team, Rating, Demo, Rater
    from django.contrib.auth.models import User
    populate()