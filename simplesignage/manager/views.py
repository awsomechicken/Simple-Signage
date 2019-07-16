from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from . import urls
import os, time, datetime, json, random

# Database implementation:
# https://docs.djangoproject.com/en/2.2/intro/tutorial02/
from manager.models import File, Show

#_______________________________________________________________________________
# primary interface stuffs:

#@login_required
def index(request):
    resp = HttpResponse("Please Hold, Development in progress...")
    return resp

# home / main data interface
@login_required
def home(request):
    print("Home", str(request.META['REMOTE_ADDR']))
    # content is passed into render, and can be parsed by the template

    content = getContent(request)

    return render(request, 'index.html', content)

#_______________________________________________________________________________
# File dealings:

def upload_file(request):
    if request.method == 'POST':
        print("file upload requested") # indform the log...
        g = request.FILES['fileupload'] # get the file the user sent
        print("Length of files: ", len(g)) # see if there is data
        handle_file(fdup_file = g) # do things with the file

    return redirect('.') # redirect to the top of the page (_self)

# file handling functionality:
def handle_file(fdup_file):
    # method to recieve and deal with files:
    # > recieve and store
    # > build database entry
    print(fdup_file)
    loc = "./manager/static/content/"+str(random.randrange(1,1800))+str(fdup_file).replace(' ','')

    # make file:
    #open(loc, 'x')

    # rebuild data as the user said:
    with open(loc, 'wb+') as dest:
        for chunk in fdup_file.chunks():
            dest.write(chunk)
        #dest.close()

    if ".zip" in str(fdup_file):
        print("We got a biggn")
    print("file uploaded, please add other database stuff")

#_______________________________________________________________________________
# Settings Managemnt Routines:

# Apply selection of images
def apply_changes(request):
    changes = request.POST
    print(changes)
    try:
        with open('./manager/static/post.json','a') as file:
            file.write(str(changes))
            file.close()
    except FileNotFoundError:
        with open('./manager/static/post.json', 'w') as file:
            file.write(str(changes))
            file.close()
        print("Whoops")
    print("HI!")
    # rather than changing the page, redirect to self,
    # must return something
    return redirect('.')

def getContent(request):
    #print(File.objects.all())
    rem_addr = request.META.get('REMOTE_ADDR')

    # content template:
    content = {
        'File':[],
        'os':time.time(),
        'you':rem_addr
    }

    # get list of images, build web content
    gottenFiles = os.listdir('./manager/static/content')
    for file in gottenFiles: # fill images into the template
        content['File'].append({'path':file,'image':True,'pdf':True,'video':True,'use':False,'startDate':'2019-06-24','endDate':'2019-12-30','deleteOnEnd':True})

    #print(content)
    return content

#_______________________________________________________________________________
# authentication methods:

def login(request):
    print("Logging In?")
    print(request.POST)
    resp = HttpResponse("Hello there")

    return render(request, 'login.html', {})

def loginauth(request):
    if request.method == 'POST':
        resp = HttpResponse("Hello there")
        print(request.POST)
    else:
        resp = HttpResponse("404: Piss off you wanker")

    return resp
