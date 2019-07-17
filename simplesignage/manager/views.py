from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from . import urls
import os, time, json, random
#pdf2image # used to convert PDFs to images for the video
try:
    import commands
except:
    print("please install module \'commands\'\n\t~$ pip(3) install commands\n")
#

# Database implementation:
# https://docs.djangoproject.com/en/2.2/intro/tutorial02/
from manager.models import Content, Show

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
@login_required
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
    filename = str(fdup_file).replace(' ','_')

    # now build the entry:
    item = Content(
        imageName = "ThisWillBeFilled", # the 'c' tag needs to reflect doc type
        uploadDate = timezone.now(),
        startDate = timezone.now(),
        expireDate = timezone.now() + timezone.timedelta(days=7), # today + 7 days
        displayTime = 25, # seconds
        order = 0
        )
    item.save() # save the item to get an ID,
    dire = item.id # use the ID to make a directory
    print("Item number:", dire) # debug
    item.imageName = "./manager/static/content/c%i/%s"%(dire, filename) # update the file location
    item.save() # resave


    success = False
    counts = 0 # loop counts
    while (not success) and (counts < 10):
        # make the directory in static:
        try:
            os.mkdir("./manager/static/content/c%i/"%(dire))
            success = True # say something if directory was made
        except FileExistsError:
            print("#%i -- directory: \"./manager/static/content/%i/\" exists, Removing"%(counts,dire))
            os.remove("./manager/static/content/c%i/"%(dire))
            counts += 1

    # build file location
    loc = "./manager/static/content/c%s/%s"%(dire, filename)

    # make file:
    #open(loc, 'x')

    # rebuild data as the user said:
    with open(loc, 'wb+') as dest:
        for chunk in fdup_file.chunks():
            dest.write(chunk)
        dest.close()

    if ".zip" in str(fdup_file):
        print("We got a biggn, needs to be unzipped and analized")
    print("file uploaded, please add other database stuff")

#_______________________________________________________________________________
# Settings Managemnt Routines:
@login_required
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

@login_required
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

    # retrieve data form the database:
    q = Content.objects.all() # quiries
    for item in q:
        obj = {
            'path':item.imageName,
            'startDate':item.startDate,
            'endDate':item.expireDate,
            'use':False,
            'deleteOnEnd':True
        }
        print(obj)
        #print("Item: %i, Path:\"%s\" "%(item.id, item.imageName))


    #print(content)
    return content
