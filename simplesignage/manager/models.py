from django.db import models
from django import forms
from django.utils.timezone import now
import random, time
from datetime import datetime
# Create your models here.
# modles define feilds and tables.

# shows and presentation models
class Show(models.Model):
    # slide show model, shows the file with these details
    name = models.CharField('Show Name', default="Slide Show Name", max_length=255)
    file = models.CharField('File Location', default="static/shows", max_length=255) # video file location

# content models:
class Content(models.Model):
    # image / file model database
    imageName = models.CharField("File Image Name", max_length=1024)
    file = models.CharField("File Location", max_length=1024, default="static/content") # upload_to='static/content'
    uploadDate = models.DateTimeField("Upload Date") # date the file was uploaded
    startDate = models.DateTimeField("Start Date") # date the file is to begin
    expireDate = models.DateTimeField("Expire Date") # Date the file will be deleted form the system to save space
    displayTime = models.IntegerField("Display Time (Seconds)", default=5) # time to show the picture / document / etc.
    gifIteration = models.IntegerField("GIF repeat count", default=1) # times to repeat the gif
    order = models.CharField("Special Order", default="-1", max_length=255) # the order in which to display, -1 = No special order
    useInShow = models.BooleanField("Use in Show", default=False)
    deleteOnExpire = models.BooleanField("Delete on Expire", default=True)

class Screen(models.Model):
    # screens, for use by compile and apply
    tvName = models.CharField("Name", max_length=200)
    hostIP = models.CharField("Host Addr. or IP:", default="192.168.0.X", max_length=2000)
    width = models.IntegerField("Screen Width", default=1920)
    height = models.IntegerField("Screen Height", default=1080)
    key = models.CharField("Key", max_length=48, default="FILL")
    useSchedule = models.BooleanField("Use Schedule", default=False)
    startTime = models.DateTimeField("TV On Time", default=datetime.now, blank=True)
    endTime = models.DateTimeField("TV On Time", default=datetime.now, blank=True)
