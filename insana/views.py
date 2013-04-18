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

from lib.asanaHelper import AsanaClient


def home(request):
    if request.user.is_authenticated():
        return _logged_in_home(request)
    else:
        return _logged_out_home(request)

def logout_view(request):
    logout(request)
    return redirect('/')

def _logged_in_home(request):
    c = RequestContext(request)
    profile = request.user.profile    
    client = AsanaClient(profile)

    workspaces = client.get_workspaces()
    if len(workspaces) > 0:
        workspace = workspaces[0].get('id')
    else:
        return redirect('/logout')

    if not request.session.get('user_projects'):
        request.session['user_projects'] = client.get_projects_for_user(workspace)

    c['user_projects'] = request.session['user_projects']
    c['default_user_project'] = c['user_projects'][0].get('name')
    del c['user_projects'][0]
    return render_to_response('logged_in_home.html', c)

def _logged_out_home(request):
    c = RequestContext(request)

    c['redirect_uri'] = constants.redirect_uri
    c['client_id'] = constants.ASANA_CLIENT_ID
    return render_to_response('landing.html', c)

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
        raise Exception('something went wrong')

    asana_access_token = asana_info.get('access_token')
    asana_refresh_token= asana_info.get('refresh_token')
    
    asana_id = asana_data.get('id')
    email = asana_data.get('email')
    name = asana_data.get('name')
    
    #create user if doesn't exist
    profiles = Profile.objects.filter(asana_id=asana_id)
    if len(profiles) > 0:
        profile = profiles[0]
    else:
        # i hate django usernames. so fuck that.
        profile = Profile.create_new_user(asana_id, name, asana_id, asana_access_token, asana_refresh_token, email)
        #set up workspaces
        
    profile.backend = 'django.contrib.auth.backends.ModelBackend'    
    login(request, profile)

 #   client = AsanaClient(profile)
#    workspaces = client.get_workspaces()
    
    return redirect('/')

