import os

def populate():
    python_cat = add_cat(name="Python",
                         views=128,
                         likes=64)
    
    add_page(cat=python_cat,
             title="Official Python Tutorial",
             url="http://docs.python.org/2/tutorial/")
    
    add_page(cat=python_cat,
             title="how to think like a computer scientist",
             url="http://www.greenteapress.com/thinkpython/")
    
    add_page(cat=python_cat,
             title="learn python in 10 minutes",
             url="http://www.korokithakis.net/tutorials/python/")
    
    django_cat = add_cat(name="Django",
                         views=100,
                         likes=50)
    
    add_page(cat=django_cat,
             title="Official Django Tutorial",
             url="http://docs.djangoproject.com/en/1.6/intro/tutorial01/")
    
    add_page(cat=django_cat,
             title="django rocks",
             url="http://www.djangorocks.com/")
    
    add_page(cat=django_cat,
             title="how to tango with django",
             url="http://www.tangowithdjango.com/")
    
    frame_cat = add_cat(name="other frameworks",
                        views=50,
                        likes=10)
    
    add_page(cat=frame_cat,
             title="Bottle",
             url="http://www.bottlepy.org/docs/dev")
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))
            
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name,views=views, likes=likes)[0]
    return c

if __name__ == '__main__':
    print "Starting Rango population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango.settings')
    from rango.models import Category, Page
    populate()