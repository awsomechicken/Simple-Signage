from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from threading import Thread
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
# ToDo: form with delete button externally, to accomplish the same thing as delete-apply

try:
    import subprocess
except:
    print("\'Subprocess\'~$ package isn't installed [ https://pymotw.com/2/subprocess/ ].\n\t please install: pip(3) install subprocess\n")

try:
    import schedule
except Exception as e:
    print("\'Scheduler\' package isn't installed [ https://github.com/dbader/schedule ].\n\t please install: ~$ pip(3) install scheduler")


# Database implementation:
# https://docs.djangoproject.com/en/2.2/intro/tutorial02/
from manager.models import Content, Show, Screen

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
    #print("Home", str(request.META['REMOTE_ADDR']))
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
            displayTime = 5, # seconds
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
        if (".mp4" or ".mpg") in filename.lower():
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
# Screen settings

@login_required
def screens(request):
    print("SCREENS!")

    content = {
        'screens': [],
        'msg':'HI!'
    }

    # get the screens:
    s = Screen.objects.all().order_by('id')

    for item in s:
        content['screens'].append({
            'id' : item.id,
            'name' : item.tvName,
            'addr' : item.hostIP,
            'width': item.width,
            'height': item.height
        })

    return render(request, 'screens.html', content)

def screenSettings(request):
    print("screen settings")

@login_required
def newScreen(request):
    # save a new screen
    screen = request.POST
    name = screen.getlist('name')[0]
    addr = screen.getlist('addr')[0]
    width = screen.getlist('width')[0]
    height = screen.getlist('height')[0]

    print("Recieved:", name, addr, width, height)

    new = Screen(tvName = name, hostIP = addr, width=width, height=height)
    new.save()

    return redirect('/screens')

@login_required
def deleteScreen(request):
    # Delete a screen db entry
    screenid = request.POST.getlist("Delete")[0]

    rem = Screen.objects.get(id__exact=screenid)
    rem.delete()
    print("delete:", screenid)

    return redirect("/screens")
#_______________________________________________________________________________
# Media Creation things

def get_mp4_thumbnail(file="./static/content/animals-Imgur.mp4"):
    #abspath = str(os.path.abspath(file)) #
    rel_path = file[1:file.rindex('/')] # get the path and file split
    file = file[file.rindex('/')+1:len(file)]

    #print(abs_pth, abspath.rindex('/')-len(abspath), file)
    thumbnail = VM.get_thumbnail(abs_path=rel_path, file_name=file)
    return thumbnail

@login_required
def make_video(request):
    print("Compile Video")
    # get your content hat is selected:
    slides = Content.objects.filter(useInShow=True)
    #print(slides)
    # add a show entry:

    # compile_video(show_items={}, output_path='./static/shows/', frame_rate=30)
    videoFilePath = VM.compile_video(show_items=slides)

    return redirect('.')

def status(request):
    print(request.method)
#_______________________________________________________________________________
# Settings Managemnt Routines:
@login_required # Apply selection of images
def apply_changes(request):
    changes = request.POST
    log_applied_changes(changes)

    cid = changes.getlist('cid')
    sdate = changes.getlist('sdate')
    edate = changes.getlist('edate')
    dispTime = changes.getlist('dispTime')
    use = changes.getlist('use')
    delOnEnd = changes.getlist('deleteOnEnd')

    #print(cid)
    for i in range(0, len(cid)): # adjust dates and dt
        item = Content.objects.get(id=cid[i])
        item.startDate = sdate[i]
        item.endDate = edate[i]
        item.displayTime = dispTime[i]
        item.save() # save the entries

    # determine if in delOnEnd:
    if len(delOnEnd) > 0:
        for e in cid:
            item = Content.objects.get(id=e)
            if e in delOnEnd:
                item.deleteOnExpire = True
            else:
                item.deleteOnExpire = False
            item.save() # save the entry

    # determine if in use:
    if len(use) > 0:
        for e in cid:
            item = Content.objects.get(id=e)
            if e in use: # if the element is in Use:
                item.useInShow = True # show
            else:
                item.useInShow = False # don't show
            item.save() # save the entry

    try: # try to delete things,
        if len(request.POST.getlist('Delete')) > 0:
            print("Deleting Things")
            delete_content(request)
    except Exception as e: # otherwise don't delete things
        print("Not deleting things")
        print(e)

    # rather than changing the page, redirect to self,
    # must return something
    return redirect('.')

def log_applied_changes(changes):
    # log the post to a file for later analysis
    try:
        with open('./manager/static/post.json','a') as file:
            file.write(str(changes))
            file.close()
    except FileNotFoundError:
        with open('./manager/static/post.json', 'w') as file:
            file.write(str(changes))
            file.close()
        print("Whoops")

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
        #print(entry.id, ':', entry.imageName, entry.expireDate.date())
        content['File'].append({
            'cid':entry.id,
            'path':entry.imageName.replace("./manager/static/content/", ""),
            'filePath':entry.file.replace("./manager/static/content/", ""),
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
    #Entry.objects.filter(pub_date__lte='2006-01-01')
    files = Content.objects.all().order_by("expireDate")

    if len(files) > 0:
        print("purging expired content")
        for entry in files:
            print(entry.id, ':', entry.imageName, entry.expireDate.date(), timezone.now().date())
            #delete_worker(entry)


def delete_content(request):
    deletion = request.POST.getlist('Delete')
    log_applied_changes(deletion)
    # get the content we want to delete
    for dele in deletion:
        remove = Content.objects.get(id__exact=dele)
        print("Delete:",remove.imageName)

        delete_worker(remove)

    # redirect to the same page
    return redirect('.')

# actual reusable worker
def delete_worker(dbEntry):
    # Pass DJango DB object into, and things go away
    # use OS remove_dir to delete the whole directory
    directory = dbEntry.imageName[0:dbEntry.imageName.rindex('/')+1]
    print(directory)
    # first delete the contents:
    try: # try delete image file
        os.remove(dbEntry.imageName)
    except Exception as e:
        print('\n\n%s\n\n'%e)

    try: # try delete file file
        print("\ndelete:%s"%dbEntry.file)
        os.remove(dbEntry.file)
    except Exception as e:
        print('\n%s\n\n'%e)

    # then delete the directory:
    os.rmdir(directory)

    # remove the database entry
    dbEntry.delete()


#_______________________________________________________________________________
# Initalize Scheduling with the Schedule module:

def schedule_check():
    #schedule.every(1).day.at("01:15").do(upkeep)
    schedule.every(1).minute.do(upkeep).run() # remove run in production

    while(True):
        with open("./threadcheck.txt", "w+") as f:
            f.write(str(time.time()))
            f.close()
        schedule.run_pending() # quirie the schedule
        time.sleep(1) # wait a bit, keep CPU load low

def schedule_thread():
    print("running schedule thread")
    thr = Thread(target=schedule_check, daemon=True)
    thr.start()

schedule_thread()
