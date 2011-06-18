from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('safeweb.views',
    url(r'^register/$', 'register', name='register'),
    url(r'^update/$', 'update', name='update'),
    url(r'^confirm/$', direct_to_template, 
            {'template': 'confirm.html'}, name='confirm'),
)
