from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, context
from . import urls
import os, time, datetime, json

# Database implementation:
# https://docs.djangoproject.com/en/2.2/intro/tutorial02/
from manager.models import File, Show

# Create your views here.
def index(request):
    resp = HttpResponse("Please Hold, Development in progress...")
    return resp

# home / main data interface
def home(request):
    print("Home", str(request.META['REMOTE_ADDR']))
    # content is passed into render, and can be parsed by the template
    print(len(urls.urlpatterns))

    content = getContent(request)

    return render(request, 'index.html', content)

def upload_file(request):

    print("file upload requested")

# file handling functionality:
def handle_file(request):
    # method to recieve and deal with files:
    if request.method == 'POST' and request.FILES > 0:
        print('I find file!')
    else:
        print('I no find file')


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

    # get list of images
    images = os.listdir('./manager/static/content')
    for image in images: # fill images into the template
        content['File'].append({'path':image,'use':False,'startDate':'2019-06-24','endDate':'2019-12-30','deleteOnEnd':True})

    print(content)
    return content
