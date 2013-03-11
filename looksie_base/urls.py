from django.conf.urls import patterns, url
urlpatterns = patterns('looksie_base.views',
    url(r'^$', 'index', name='index'),
    url(r'^create/$', 'create', name='create'),
    url(r'^edit/(?P<imageUuid>[a-f0-9]+)/$', 'edit', name='edit'),
    url(r'^embed/(?P<imageUuid>[a-f0-9]+)/$', 'embed', name='embed'),
    url(r'^list/$', 'list', name='list'),
)
