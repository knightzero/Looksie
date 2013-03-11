from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('looksie_api.views',
    # redirects the user to the link
    url(r'^link/(?P<linkUuid>[a-f0-9]+)/$', 'link'),
    # gets all images of a user
    url(r'^get/all/$', 'getall'),
    url(r'^get/jsonp/all/$', 'getalljsonp'),
    # gets one image of a user
    url(r'^get/(?P<ImageUuid>[a-f0-9]+)/$', 'get'),
    url(r'^get/jsonp/(?P<ImageUuid>[a-f0-9]+)/$', 'getjsonp'),
    url(r'^get/html/(?P<ImageUuid>[a-f0-9]+)/$', 'gethtml'),
    # saves and dots image
    url(r'^post/$', 'post'),
    
    # save images & dots, just dots, just images
    url(r'^save/image/$', 'save', name='api.save'),
    url(r'^save/dots/(?P<imageUuid>[a-f0-9]+)/$', 'save', name='api.save.dots'),
    # update images & dots, just dots, just images
    url(r'^update/image/(?P<imageUuid>[a-f0-9]+)/$', 'update', name='api.update'),
    url(r'^update/dots/(?P<dotUuid>[a-f0-9]+)/$', 'update', name='api.update.dots'),
   
    # delete images & dots, just dots, just images
    url(r'^delete/image/(?P<imageUuid>[a-f0-9]+)/$', 'delete', name='api.delete'),
    url(r'^delete/dots/(?P<dotUuid>[a-f0-9]+)/$', 'delete', name='api.delete.dots'),
)