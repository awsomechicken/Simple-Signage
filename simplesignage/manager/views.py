from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader, context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# http://code.djangoproject.com/browser/django/trunk/django/contrib/admin/views/decorators.py
#from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.views.static import serve
# password reset things
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# non-django related things:
from threading import Thread
from . import urls
import os, time, datetime, json, random, string, shutil
#pdf2image is used to convert PDFs to images for the video
from pdf2image import convert_from_path
from PIL import Image # PIL for saving the picture
import tempfile
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
# ToDo: form with delete button externally, to accomplish the same thing as delete-apply
from zipfile import ZipFile

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
# global variables for things:

Video_Compiling = False

#_______________________________________________________________________________
# primary interface stuffs:
# password reset form
@login_required
def passwd_change(request):
    # code from: https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

#@login_required
###@staff_member_required
def index(request):
    resp = HttpResponse("<h1>Error 909: Development Whilst Drunk Occured</h1><h2>apologies for any inconveniece</h2><hr>")
    return resp, redirect('/')

# home / main data interface
@login_required
###@staff_member_required
def home(request):
    #print("Home", str(request.META['REMOTE_ADDR']))
    # content is passed into render, and can be parsed by the template

    content = getContent(request)

    return render(request, 'index.html', content)

# documentation senction, over by the admin page link
def documentation(request):
    resp = HttpResponse("documentation here...")

    return render(request, 'documentation.html')
#_______________________________________________________________________________
# File dealings:
@login_required
###@staff_member_required

def upload_file(request):
    if request.method == 'POST':
        try: # to mitigate the no file found error
            print("file upload requested") # indform the log...
            g = request.FILES['fileupload'] # get the file the user sent
            print("Length of files: ", len(g)) # see if there is data
            handle_file(fdup_file = g) # do things with the file
        except Exception as e: # don't do a damn thing
            print("No file selected, not trying to handle it.")
            print(e)
    return redirect('.') # redirect to the top of the page (_self)

# file handling functionality:
def handle_file(fdup_file):
    # method to recieve and deal with files:
    # > recieve and store
    # > build database entry
    print(fdup_file)
    filename = str(fdup_file).replace(' ','_') # replace whitespace with underscores

    if ".zip" in str(fdup_file):
        print("We got a biggn, needs to be unzipped and analized")
        handle_zipped_file(filename, fdup_file)

    else: # not a ZIP file, so behave in a one-off manner:
        make_db_entry(filename, fdup_file)

def handle_zipped_file(filename, fdup_file):
    print("handling zipped file")
    # store the zip temporaraly
    temp_file = "./manager/static/content/%s"%(filename)
    temp_dir = "./manager/static/content/%s"%(filename).replace(".zip", "").replace("_", ' ')
    # rebuild the file from the chunks
    print(fdup_file)
    rebuild_fdup_data(loc=temp_file, chunky_file=fdup_file) # save the data to the system
    # extract the jeezless thing:
    with ZipFile(temp_file, 'r') as zipObj:
        zipObj.extractall(temp_dir) # extract the objects

    # see what we have:
    extracted = os.listdir(temp_dir)
    print('Extracted:', extracted)
    #chunksize = 256 # bytes per chunk
    for file in extracted:
        print('loop', temp_dir, file)
        pth = "%s/%s"%(temp_dir, file)
        print(pth)

        make_db_entry(file, single_file = False, temp_path = pth)


    # cleanup the directory
    os.remove(temp_file)
    shutil.rmtree(temp_dir)


def make_db_entry(filename, fdup_file = None, single_file = True, temp_path = None):
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

        if single_file: # if it is a single file from the web interface do this:
            rebuild_fdup_data(loc, fdup_file)
        else:  # used for zip files, because the data is already reconstructed:
            #copy_data_from_temp_path()
            shutil.copy(temp_path, loc)


        # find how the video will be previewed:
        if (".mp4") in filename.lower():
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

        elif ".png" or ".jpg" or ".gif" in filename.lower():
            print("This must be an image...")
            item.imageName = loc
            item.file = loc
            item.save()
            print("Image saved")

def rebuild_fdup_data(loc, chunky_file):
    # rebuild data as the user said:
    with open(loc, 'wb+') as dest:
        for chunk in chunky_file.chunks():
            dest.write(chunk)
        dest.close()

#_______________________________________________________________________________
# Screen settings

# TV token authentication decoration:
def token_authorization(func):
    def function_wrapper(req): # wrapper for the request stuffs (I think)
        try:
            key = req.GET.getlist('auth_token')[0] # get the key
        except:
            key = "None Found"
        print("auth_token =", key)

        appscreen = Screen.objects.filter(key=key) # filtered screen list
        key_check = ''
        for s in appscreen:
            key_check = s.key
            print("Key check:", key_check)

        if key_check == key:
            return func(req)
        else:
            raise PermissionDenied
            print(datetime.datetime.now(), "Unauthroizes access prevented from:", req.get_host())

    return function_wrapper


@login_required
##@staff_member_required
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
            'height': item.height,
            'useSched':item.useSchedule,
            'starttime':item.startTime.strftime("%H:%M"),
            'endtime': item.endTime.strftime("%H:%M"),
            'key' : item.key
        })

    return render(request, 'screens.html', content)

def screenSettings(request):
    # used to update screen settings
    print("screen settings")

def screen_active_hours(request):
    print("active hours")

@login_required
##@staff_member_required
def newScreen(request):
    # save a new screen
    screen = request.POST
    name = screen.getlist('name')[0]
    addr = screen.getlist('addr')[0]
    width = screen.getlist('width')[0]
    height = screen.getlist('height')[0]

    #print("Recieved:", name, addr, width, height)

    new = Screen(tvName = name, hostIP = addr, width=width, height=height, key=make_tv_key())
    new.save()

    return redirect('/screens')

@login_required
##@staff_member_required
def deleteScreen(request):
    # Delete a screen db entry
    screenid = request.POST.getlist("Delete")[0]

    rem = Screen.objects.get(id__exact=screenid)
    rem.delete()
    print("delete:", screenid)

    return redirect("/screens")

def make_tv_key():
    len = 48 # length of the key
    ky = ''.join(random.choices(string.ascii_letters + string.digits, k=len))

    return ky

# public facing content delivery methods, using token auth.
@token_authorization
def get_tv_video(request):
    # counterpart for the get_video method in simpleviewer

    print("transmitting video file")
    fileToTXDir = os.path.dirname(Show.objects.all()[0].file)
    fileToTXName = os.path.basename(Show.objects.all()[0].file)
    # from: https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
    file_to_Serve = serve(request, fileToTXName, fileToTXDir)


    return file_to_Serve

@token_authorization
def check_new_video(request):
    # check if there is a new video for the screens
    print(request.POST.getlist('auth_token'))
    curr_show = Show.objects.all()[0].name # get the current show name, Screens will compare theirs to it.
    return HttpResponse(curr_show) # send a response containing the name of the show

# screen quiry for settings:
@token_authorization
def newSettingsForMe(request):
    # ses
    tok = request.GET.getlist('auth_token')[0]

    tv = Screen.objects.filter(key__exact = tok)[0]

    print(tv)

    tvSettings = {
        'width' : tv.width,
        'height': tv.height,
        'useSched' : tv.useSchedule,
        'startTime': tv.startTime,
        'endTime' : tv.endTime
    }

    return JsonResponse(tvSettings)

# mkae changes to the tv settings
def tvSettingsChange(request):
    tvId = request.POST.getlist('tv.id')[0]
    tvAdd = request.POST.getlist('tv.address')[0]
    #tvWidth = request.POST.getlist('tv.width')[0]
    #tvHeight = request.POST.getlist('tv.height')[0]
    try: # boolean values don't exist if they aren't checked...
        tvUseSched = request.POST.getlist('tv.useSched')[0]
    except:
        tvUseSched = 0 # do a 0, it makes things easier
    tvStartTime = request.POST.getlist('tv.starttime')[0]
    tvEndTime = request.POST.getlist('tv.endtime')[0]
    # int(tvWidth), int(tvHeight),
    print(tvId, tvAdd, tvUseSched, tvStartTime, tvEndTime)

    # updae / add information:
    tv = Screen.objects.filter(id__exact=tvId)[0]
    tv.hostIP = tvAdd # set TV address
    #tv.width = int(tvWidth)
    #tv.height = int(tvHeight)
    if int(tvUseSched) > 0:
        tv.useSchedule = True # boolean Value, I don't know how this uses
    else:
        tv.useSchedule = False
    tv.startTime = datetime.datetime.strptime(tvStartTime, '%H:%M')
    tv.endTime = datetime.datetime.strptime(tvEndTime, '%H:%M')
    tv.save()

    return redirect('/screens')

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
##@staff_member_required
def make_video(request):

    videoFilePath = make_video_worker()

    return HttpResponse("<h2>Show accelerated video: %s</h2> <p><a href=\"/\">Go Back</a><p>"%videoFilePath) #redirect('.')

def make_video_worker():
    # reusable worker!
    print("Compile Video")
    # get your content hat is selected:
    slides = Content.objects.filter(useInShow=True)
    #print(slides)
    # add a show entry:

    # compile_video(show_items={}, output_path='./static/shows/', frame_rate=30)
    global Video_Compiling
    Video_Compiling = True # indicate the video is compiling

    print("video compiling:", Video_Compiling)
    videoFilePath, new_show_name = VM.compile_video(show_items=slides)
    new_show = Show(name = new_show_name, file = videoFilePath)
    new_show.save()

    Video_Compiling = False # indicate the video is done

    print("video compiling:", Video_Compiling)

    # purge old shows:
    shows = Show.objects.all()

    for item in shows: # for every old show:
        if item.name != new_show_name: # if it isn't the newest
            os.remove(item.file) # delete the video file
            item.delete() # get rid of the DB entry

    return videoFilePath # return a thing for use by routines...

def video_compile_status(request):
    # routine for showing the status of the video comnpile for the UI,
    # so the user doens't get frustrated
    print(request.method)
    status = HttpResponse("%s"%(Video_Compiling))

    return status

#_______________________________________________________________________________
# Settings Managemnt Routines:
@login_required
##@staff_member_required # Apply selection of images
def apply_changes(request):
    changes = request.POST
    #log_applied_changes(changes)
    cid = changes.getlist('cid')
    sdate = changes.getlist('sdate')
    edate = changes.getlist('edate')
    dispTime = changes.getlist('dispTime')
    gifIteration = changes.getlist('gifIteration')
    print("GIFs:", gifIteration)
    use = changes.getlist('use')
    delOnEnd = changes.getlist('deleteOnEnd')

    #print(cid)
    for i in range(0, len(cid)): # adjust dates and dt
        item = Content.objects.get(id=cid[i])
        item.startDate = sdate[i]
        item.expireDate = edate[i]
        try:
            dt = dispTime[i]
            if dt < 301:
                item.displayTime = dt
            else:
                item.displayTime = 300
        except:
            pass
        try:
            gi = int(gifIteration[i])
            if gi < 301:
                item.gifIteration = gi
            else:
                item.gifIteration = 300
        except:
            pass

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
##@staff_member_required
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
            # strip off some of the non-pertanant information in the files and images
            'path':entry.imageName.replace("./manager/static/content/", ""),
            'filePath':entry.file.replace("./manager/static/content/", ""),
            'use':entry.useInShow,
            'startDate':str(entry.startDate.date()),
            'endDate':str(entry.expireDate.date()),
            'gifIteration':entry.gifIteration,
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
    # get the contents that are to be deleted on expire date
    files = Content.objects.filter(deleteOnExpire=True).order_by("expireDate")
    # get the current date for use later:
    currentTime = timezone.now()
    deletecount = 0
    if len(files) > 0:
        print("looking for expired content")
        for entry in files:
            #print(entry.id, ':', entry.imageName, 'Expire:', entry.expireDate, 'Now:', currentTime)
            if currentTime.date() >= entry.expireDate.date():
                print("Deleting expored content: c%d"%(entry.id))
                delete_worker(entry)
                deletecount += 1 # increment the number of deleted things

    if deletecount > 0:
        # then recompile video
        make_video_worker()

# when the delete button is pressed, this happens:
def delete_content(request):
    deletion = request.POST.getlist('Delete')
    #log_applied_changes(deletion)
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

    try: # try delete file file, if no file file, the an error will arise
        print("\ndelete:%s"%dbEntry.file)
        os.remove(dbEntry.file)
    except Exception as e: # then handle it...
        print('\n%s\n\n'%e)

    # then delete the directory:
    os.rmdir(directory)

    # remove the database entry
    dbEntry.delete()


#_______________________________________________________________________________
# Initalize Scheduling with the Schedule module:

def schedule_check():
    # schedule upkeep to run every day at 03:30 in the morning
    schedule.every().day.at('01:30').do(upkeep).run() # remove run in production

    while(True):
        #with open("./threadcheck.txt", "w+") as f:
        #    f.write(str(time.time()))
        #    f.close()
        schedule.run_pending() # quirie the schedule
        time.sleep(1) # wait a bit, keep CPU load low

def schedule_thread():
    print("running schedule thread")
    thr = Thread(target=schedule_check, daemon=True)
    thr.start()

schedule_thread()
