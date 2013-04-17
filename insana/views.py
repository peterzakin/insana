from django.contrib.auth import authenticate, login
import sys
import string
import re

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import logout


def home(request):
    c = RequestContext(request)
    c['peter'] = 'HELLO PETER'
    return render_to_response('landing.html', c)

def logout(request):
    logout(request)
    return redirect('/')

def _logged_in_home(request):
    pass

def _logged_out_home(request):
    pass
