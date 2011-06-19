from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('safeweb.views',
    url(r'^register/$', 'register', name='register'),
    url(r'^update/$', 'update', name='update'),
    url(r'^confirm/$', direct_to_template, 
            {'template': 'confirm.html'}, name='confirm'),
    url(r'^safe/$', direct_to_template, {'template': 'safe.html'}, name='safe'),
    url(r'^updated/$', direct_to_template, {'template': 'updated.html'}, name='updated'),
    url(r'^help/(?P<traveller_id>\d+)/$', 'help', {'country': None}, name='help'),
    url(r'^help/(?P<traveller_id>\d+)/(?P<country>\w\w)/$', 'help', name='help-country'),
    url(r'^country/(?P<country>\w\w)/$', 'country_summary', name='country-summary'),
)
