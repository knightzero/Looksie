from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from looksie_api.functions import encodeImageJson, encodeImageJsonp
import uuid
from looksie_base.models import Dot, Image
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.utils import simplejson


@cache_page(60*15)
def images(request, apiType=None, imageUuid=None):
    if imageUuid is not None:
        images = get_object_or_404(Image, uuid=imageUuid)
    else:
        try:
            session = Session.objects.get(pk=request.session.session_key)
        except:
            raise Http404
        else:
            images = Image.objects.filter(session=session)
    if apiType.lower() == 'json':
        data = encodeImageJson(images)
        return HttpResponse(data, mimetype='application/json')
    elif apiType.lower() == 'jsonp':
        data = encodeImageJsonp(images, request)
        return HttpResponse(data, mimetype='application/javascript')
    elif apiType.lower() == 'xml':
        return render_to_response('api/xml/images.xml', {'images': images}, context_instance=RequestContext(request), mimetype="application/xhtml+xml" )
    raise Http404