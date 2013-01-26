from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('webapp.views',
    url(r'', include('singly.urls')),
    url(r'^$', 'index', name='index'),
    url(r'query$', 'query', name='query'),
    url(r'manifest.json$', 'manifest')

)
