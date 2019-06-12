from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os, time, datetime
#from django import file

# Create your views here.
def index(request):
    resp = HttpResponse("Please Hold, Development in progress...")
    return resp

# home / main data interface
def home(request):
    rem_addr = request.META.get('REMOTE_ADDR')
    print("Home", str(request.META['REMOTE_ADDR']))
    # content is passed into render, and can be parsed by the template
    content = {'File':os.listdir('..'),'os':time.time(),'you':rem_addr}

    return render(request, 'index.html', content)

# file handling functionality:
def filehandle(request):

    pass

# Apply selection of images
def apply_changes(request):
    print("HI!")
