from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from . import urls
import os, time, json, random
#pdf2image # used to convert PDFs to images for the video
from pdf2image import convert_from_path
from PIL import Image # PIL for saving the picture
import tempfile
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

try:
    import commands
except:
    print("please install module \'commands\'\n\t~$ pip(3) install commands\n")
#

# Database implementation:
# https://docs.djangoproject.com/en/2.2/intro/tutorial02/
from manager.models import Content, Show

# video lib:
from . import VideoMaker as VM

#_______________________________________________________________________________
# primary interface stuffs:

#@login_required
def index(request):
    resp = HttpResponse("<h1>Error 909: Development Whilst Drunk Occured</h1><h2>apologies for any inconveniece</h2><hr>")
    return resp, redirect('/')

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

    if ".zip" in str(fdup_file):
        print("We got a biggn, needs to be unzipped and analized")

    else: # not a ZIP file, so behave in a one-off manner:
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
        item.file = "./manager/static/content/c%i/%s"%(dire, filename) # update the file location
        item.save() # resave

        # make a directory:
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

        # rebuild data as the user said:
        with open(loc, 'wb+') as dest:
            for chunk in fdup_file.chunks():
                dest.write(chunk)
            dest.close()


        # find how the video will be previewed:
        if ".mp4" in filename.lower():
            print("I found an MP4, getting a thumbnail...")

            thumbnail = get_mp4_thumbnail(file=item.file)
            print("I gots the thumbnail: ", thumbnail)
            item.imageName = "./manager/static/content/c%s/%s"%(dire, thumbnail)
            item.file = loc
            item.save()
            print("thumbnail saved")

        elif ".pdf" in filename.lower():
            print("Found a PDF, getting a JPG")
            try:
                jpg_path = "./manager/static/content/c%s/%s"%(dire, filename.replace('.pdf', '.jpg'))
            except:
                jpg_path = "./manager/static/content/c%s/%s"%(dire, filename.replace('.PDF', '.jpg'))

            image = convert_from_path(pdf_path=loc, dpi=200, thread_count=2, fmt='jpg', single_file=True)
            print(image[0])
            image[0].save(fp=jpg_path)

            # save the stuff to database
            item.imageName = jpg_path
            item.file = jpg_path
            item.save()

            # now delete the PDF to save space
            os.remove(loc)

        elif ".png" or ".jpg" in filename.lower():
            print("This must be an image...")
            item.imageName = loc
            item.file = loc
            item.save()
            print("Image saved")


#_______________________________________________________________________________
# Media Creation things

def get_mp4_thumbnail(file="./static/content/animals-Imgur.mp4"):
    #abspath = str(os.path.abspath(file)) #
    rel_path = file[1:file.rindex('/')] # get the path and file split
    file = file[file.rindex('/')+1:len(file)]

    #print(abs_pth, abspath.rindex('/')-len(abspath), file)
    thumbnail = VM.get_thumbnail(abs_path=rel_path, file_name=file)
    return thumbnail

def make_video():
    print("Video")


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
    #gottenFiles = os.listdir('./manager/static/content')
    files = Content.objects.all().order_by('expireDate')
    for entry in files:
        print(entry.id, ':', entry.imageName, entry.expireDate.date())
        content['File'].append({
            'cid':entry.id,
            'path':entry.imageName.replace("./manager/static/content/", ""),
            'use':entry.useInShow,
            'startDate':str(entry.startDate.date()),
            'endDate':str(entry.expireDate.date()),
            'deleteOnEnd':entry.deleteOnExpire,
            'displayTime':entry.displayTime
        })


    #print(content)
    return content

#_______________________________________________________________________________
# content upkeep routines, used to remove old files, and refresh the slideshow
def upkeep():
    print("executing upkeep...")

def thePurge():
    print("purging expired content")

    #Entry.objects.filter(pub_date__lte='2006-01-01')
    files = Content.objects.all().order_by('expireDate')

    for entry in files:
        print(entry.id, ':', entry.imageName, entry.expireDate.date())

@login_required
def delete_content(request):
    deletion = int(request.POST['Delete'])
    # get the content we want to delete
    remove = Content.objects.get(id__exact=deletion)
    print("Delete:",remove.imageName)

    delete_worker(remove)

    # redirect to the same page
    return redirect('.')

# actual reusable worker
def delete_worker(dbEntry):
    # use OS remove_dir to delete the whole directory
    directory = dbEntry.imageName[0:dbEntry.imageName.rindex('/')+1]
    print(directory)
    # first delete the contents:
    try: # try both, because in some instances file and imageName are the same
        os.remove(dbEntry.imageName)
        os.remove(dbEntry.file)
    except:
        print('all done')

    # then delete the directory:
    os.rmdir(directory)

    # remove the database entry
    dbEntry.delete()
