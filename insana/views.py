from django.contrib.auth import authenticate, login
import sys
import string
import re
import constants
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import logout
import requests
import simplejson
from models import Profile

def home(request):
    c = RequestContext(request)
    c['peter'] = 'HELLO PETER'
    c['redirect_uri'] = constants.redirect_uri
    c['client_id'] = constants.ASANA_CLIENT_ID
    return render_to_response('landing.html', c)

def logout(request):
    logout(request)
    return redirect('/')

def _logged_in_home(request):
    pass

def _logged_out_home(request):
    pass

def asana_callback(request):
    code = request.GET.get('code')
    url = "https://app.asana.com/-/oauth_token"
    data = {
        'grant_type':'authorization_code',
        'client_id':constants.ASANA_CLIENT_ID,
        'client_secret':constants.ASANA_CLIENT_SECRET,
        'redirect_uri': constants.redirect_uri,
        'code': code,
        }
    response = requests.post(url, data=data)

    asana_info = simplejson.loads(response.text)
    asana_data = asana_info.get('data')

    if not asana_data:
        import pdb; pdb.set_trace()

    asana_access_token = asana_info.get('access_token')
    asana_refresh_token= asana_info.get('refresh_token')
    
    asana_id = asana_data.get('id')
    email = asana_data.get('email')
    name = asana_data.get('name')
    
    #create user if doesn't exist
    profile = Profile.objects.get(asana_id=asana_id)
    if not profile:
        # i hate django usernames. so fuck that.
        profile = Profile.create_new_user(asana_id, name, asana_id, asana_access_token, asana_refresh_token, email)
    
    user.backend = 'django.contrib.auth.backends.ModelBackend'    
    login(request, profile)

