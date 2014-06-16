from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'rango.views.index', name='index'),
    url(r'^about/$', 'rango.views.about', name='about'),
    url(r'^contact/$', 'rango.views.contact', name='contact'),
    

)
