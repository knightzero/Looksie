from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('looksie_api.views',
    url(r'^$', 'api'),
    url(r'^images.(?P<apiType>[a-z]+)/(?P<imageUuid>[a-f0-9]+)/$', 'images'),
    url(r'^images.(?P<apiType>[a-z]+)$', 'images'),
)