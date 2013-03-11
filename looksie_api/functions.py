from django.utils import simplejson
from looksie_base.models import Image
def encodeImageJson(images):
    if isinstance(images, Image):
        images = [images,]
    data={}
    for image in images:
        data[image.uuid] = {}
        data[image.uuid]['url'] = image.url
        data[image.uuid]['dots'] = []
        for dot in image.dot_set.all():
            dotdata = {}
            dotdata['uuid'] = dot.uuid
            dotdata['x'] = dot.x
            dotdata['y'] = dot.y
            dotdata['title'] = dot.title
            dotdata['description'] = dot.description
            dotdata['callToAction'] = dot.callToAction
            dotdata['linkHref'] = dot.linkHref
            dotdata['linkText'] = dot.linkText
            data[image.uuid]['dots'].append(dotdata)
    return simplejson.dumps(data)
    
def encodeImageJsonp(images, request=None):
    if isinstance(images, Image):
        images = [images,]
    data={}
    for image in images:
        data[image.uuid] = {}
        data[image.uuid]['url'] = image.url
        data[image.uuid]['dots'] = []
        for dot in image.dot_set.all():
            dotdata = {}
            dotdata['uuid'] = dot.uuid
            dotdata['x'] = dot.x
            dotdata['y'] = dot.y
            dotdata['title'] = dot.title
            dotdata['description'] = dot.description
            dotdata['callToAction'] = dot.callToAction
            dotdata['linkHref'] = dot.linkHref
            dotdata['linkText'] = dot.linkText
            data[image.uuid]['dots'].append(dotdata)
    if request is not None:
        jsonpCallBack = request.GET.get('jsonp', None)
        if jsonpCallBack is not None:
            data = " " + jsonpCallBack + "("+ simplejson.dumps(data) +");"
            return data
    data = "parseResponse("+ simplejson.dumps(data) +");"
    return data