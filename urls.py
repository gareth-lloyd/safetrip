from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
from safeweb import urls as safeweb_urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'home.html'}, name='home'),
    url(r'^', include(safeweb_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
