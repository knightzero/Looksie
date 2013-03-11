from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils import simplejson

import uuid
from looksie_base.models import Dot, Image

from django.views.decorators.csrf import csrf_exempt

def link(request, linkUuid):
    dot = get_object_or_404(Dot, uuid=linkUuid)
    dot.clicks+=1;
    dot.save()
    return redirect(dot.linkHref)
    
def get(request, ImageUuid):
    image = get_object_or_404(Image, uuid=ImageUuid)
    some_data = {}
    some_data['image_url'] = image.url
    some_data['uuid'] = image.uuid
    some_data['views'] = image.views
    some_data['height'] = image.height
    some_data['width'] = image.width
    some_data['links'] = []
    for dot in image.dot_set.all():
        dotdata = {}
        dotdata['id'] = dot.uuid
        dotdata['posX'] = dot.x
        dotdata['posY'] = dot.y
        dotdata['clicks'] = dot.clicks        
        dotdata['title'] = dot.title
        dotdata['description'] = dot.description
        dotdata['call_to_action'] = dot.callToAction
        dotdata['link_href'] = dot.linkHref
        dotdata['link_text'] = dot.linkText
        some_data['links'].append(dotdata)
        
    data = simplejson.dumps(some_data)
    image.views+=1;
    image.save()
    return HttpResponse(data, mimetype='application/json')
    
def getjsonp(request, ImageUuid):
    image = get_object_or_404(Image, uuid=ImageUuid)
    some_data = {}
    some_data['image_url'] = image.url
    some_data['uuid'] = image.uuid
    some_data['views'] = image.views
    some_data['height'] = image.height
    some_data['width'] = image.width
    some_data['links'] = []
    for dot in image.dot_set.all():
        dotdata = {}
        dotdata['id'] = dot.uuid
        dotdata['posX'] = dot.x
        dotdata['posY'] = dot.y
        dotdata['clicks'] = dot.clicks        
        dotdata['title'] = dot.title
        dotdata['description'] = dot.description
        dotdata['call_to_action'] = dot.callToAction
        dotdata['link_href'] = dot.linkHref
        dotdata['link_text'] = dot.linkText
        some_data['links'].append(dotdata)
        
    data = simplejson.dumps(some_data)
    image.views+=1;
    image.save()
    return HttpResponse("parseResponse("+ data +");", mimetype='application/javascript')
    
def gethtml(request, ImageUuid):
    image = get_object_or_404(Image, uuid=ImageUuid)
    image.views+=1;
    image.save()
    return render_to_response('api/gethtml.html', {'image': image}, context_instance=RequestContext(request) )
 
def getall(request):
    session = Session.objects.get(pk=request.session.session_key)
    images = Image.objects.filter(session=session)
    some_data = {}
    for image in images:
        some_data[image.uuid] = {'image_url':image.url, 'uuid': image.uuid, 'views': image.views, 'height': image.height, 'width': image.width,  'links': []}
        for dot in image.dot_set.all():
            dotdata = {}
            dotdata['id'] = dot.uuid
            dotdata['posX'] = dot.x
            dotdata['posY'] = dot.y
            dotdata['clicks'] = dot.clicks        
            dotdata['title'] = dot.title
            dotdata['description'] = dot.description
            dotdata['call_to_action'] = dot.callToAction
            dotdata['link_href'] = dot.linkHref
            dotdata['link_text'] = dot.linkText
            some_data[image.uuid]['links'].append(dotdata)
        
    data = simplejson.dumps(some_data)
    return HttpResponse(data, mimetype='application/json')

def getalljsonp(request):
    session = Session.objects.get(pk=request.session.session_key)
    images = Image.objects.filter(session=session)
    some_data = {}
    for image in images:
        some_data[image.uuid] = {'image_url':image.url, 'uuid': image.uuid, 'views': image.views, 'height': image.height, 'width': image.width,  'links': []}
        for dot in image.dot_set.all():
            dotdata = {}
            dotdata['id'] = dot.uuid
            dotdata['posX'] = dot.x
            dotdata['posY'] = dot.y
            dotdata['clicks'] = dot.clicks        
            dotdata['title'] = dot.title
            dotdata['description'] = dot.description
            dotdata['call_to_action'] = dot.callToAction
            dotdata['link_href'] = dot.linkHref
            dotdata['link_text'] = dot.linkText
            some_data[image.uuid]['links'].append(dotdata)
        
    data = simplejson.dumps(some_data)
    return HttpResponse("parseResponse("+ data +");", mimetype='application/javascript')
 
    
@csrf_exempt 
def post(request):
    if request.method == 'POST':
        json_data = simplejson.loads(request.raw_post_data)
        image = Image()
        image.url = json_data["image_url"]
        image.views = 0
        image.height = json_data["height"]
        image.width = json_data["width"]
        image.uuid = uuid.uuid1().hex
        image.user = request.user
        image.save(commit=False)
        for link in json_data['links']:
            dot = Dot()
            dot.image= image
            dot.x = link['posX']
            dot.y = link['posY']
            dot.clicks = 0
            dot.title = link['title']
            dot.description = link['description']
            dot.callToAction = link['call_to_action']
            dot.linkHref = link['link_href']
            dot.linkText = link['link_text']
            dot.uuid = uuid.uuid1().hex
            print link

 
    return HttpResponse("OK")

@csrf_exempt 
def save(request, imageUuid=None):
    Pass
            
@csrf_exempt
def update(request, imageUuid=None, dotUuid=None):
    if request.method == 'POST':
        json_data = simplejson.loads(request.raw_post_data)
        if imageUuid is not None:
            image = get_object_or_404(Image, uuid=imageUuid, user=request.user)
            image.url = json_data['url']
            image.views = json_data['views']
            image.height = json_data['height']
            image.width = json_data['width']
            image.save()
            return HttpResponse("OK")
        if dotUuid is not None:
            dot = get_object_or_404(Dot, uuid=dotUuid)
            if dot.user == request.user:
                dot.x = json_data['posX']
                dot.y = json_data['posY']
                dot.click = json_data['clicks']
                dot.title = json_data['title']
                dot.callToAction = json_data['call_to_action']
                dot.description = json_data['description']
                dot.linkHref = json_data['link_href']
                dot.linkText = json_data['link_text']
                return HttpResponse("OK")
            return HttpResponse("ERROR")
    return HttpResponse("ERROR")
    
def delete(request, imageUuid=None, dotUuid=None):
    if imageUuid is not None:
        image = get_object_or_404(Image, uuid=imageUuid, user=request.user)
        image.delete()
        return HttpResponse("OK")
    if dotUuid is not None:
        dot = get_object_or_404(Dot, uuid=dotUuid)
        if dot.user == request.user:
            dot.delete()
            return HttpResponse("OK")
    return HttpResponse("ERROR")