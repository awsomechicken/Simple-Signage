from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, context
from . import urls
import os, time, datetime, json, random

# Database implementation:
# https://docs.djangoproject.com/en/2.2/intro/tutorial02/
from manager.models import File, Show

# Create your views here.
#@login_required
def index(request):
    resp = HttpResponse("Please Hold, Development in progress...")
    return resp

# home / main data interface
def home(request):
    print("Home", str(request.META['REMOTE_ADDR']))
    # content is passed into render, and can be parsed by the template

    content = getContent(request)

    return render(request, 'index.html', content)

def upload_file(request):
    if request.method == 'POST':
        g = request.FILES['fileupload'] # get the file the user sent
        print("Length of files: ", len(g)) # see if there is data
        handle_file(fdup_file = g) # do things with the file
    print("file upload requested") # indform the log...
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
    print("file uploaded, please add other database stuff")


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
    images = os.listdir('./manager/static/content')
    for image in images: # fill images into the template
        content['File'].append({'path':image,'use':False,'startDate':'2019-06-24','endDate':'2019-12-30','deleteOnEnd':True})

    #print(content)
    return content
