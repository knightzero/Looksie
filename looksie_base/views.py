from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from decorators import anonymous_required
from django.contrib.auth.decorators import login_required
from forms import UserLoginForm, UrlForm
from django.template import RequestContext
from django.contrib import messages

import uuid

from django.contrib.sessions.models import Session
from looksie_base.models import Image

from django.views.decorators.csrf import csrf_exempt

def index(request):
    request.session.set_test_cookie()
    urlForm = UrlForm()
    return render_to_response('index.html', {'urlForm': urlForm}, context_instance=RequestContext(request) )
    
@csrf_exempt
def create(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            #urlForm = UrlForm(request.POST)
            #if urlForm.is_valid():
            image = Image()
            image.url = request.POST.get('image_url_input')
            image.uuid = uuid.uuid1().hex
            session = Session.objects.get(pk=request.session.session_key)
            image.session = session
            image.save()
            # more code gose here at some point.
            return render_to_response('create.html', {'image': image}, context_instance=RequestContext(request) )
            #else:
             #   messages.error(request, 'Invalid url, please try again.')
        else:
            messages.error(request, 'Cookies not enabled. Please enable cookies and try agin.')
    return redirect('/')

def edit(request, imageUuid=None):
    session = Session.objects.get(pk=request.session.session_key)
    image = get_object_or_404(Image, uuid=imageUuid, session=session)
    return render_to_response('edit.html', {}, context_instance=RequestContext(request) )

def embed(request, imageUuid=None):
    return render_to_response('embed.html', {}, context_instance=RequestContext(request) )
    
def list(request):
    try:
        session = Session.objects.get(pk=request.session.session_key)
    except:
        return redirect('/')
    images = Image.objects.filter(session=session)
    print images
    return render_to_response('list.html', {}, context_instance=RequestContext(request) )

# unused code
'''
@anonymous_required(home_url='/')
def logIn(request):
    userLoginForm = UserLoginForm()
    if request.method == 'POST':
        userLoginForm = UserLoginForm(request.POST)
        if userLoginForm.is_valid():
            user = authenticate(username=userLoginForm.cleaned_data['username'], password=userLoginForm.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Success: Oh yeah! <br /> It looks like you are now logged in.')
                    if request.REQUEST.__contains__('next'):
                        return redirect(request.REQUEST['next'])
                    return redirect('/')
                else:
                    messages.error(request, 'Error: Oh Noes! <br /> It looks like that user isn\'t active.')
            else:
                messages.error(request, 'Error: Oh Noes! <br /> Unknown user and password combination.')
        else:
            messages.error(request, 'Error: Oh Noes! <br /> It looks like you missed somthing, please double check the form.')
    return render_to_response('login.html', { 'userLoginForm': userLoginForm }, context_instance=RequestContext(request) )
    
@login_required(login_url='/login/')
def logOut(request):
    if request.user.is_authenticated():
        logout(request)
        messages.success(request, 'Success: Oh yeah! <br /> You are now logged out.')
    return redirect('/')
'''