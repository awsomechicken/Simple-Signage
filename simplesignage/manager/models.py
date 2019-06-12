from django.db import models
from django import forms
import random, time, datetime
# Create your models here.
# modles define feilds and tables.

# shows and presentation models
class Show(models.Model):
    # slide show model, shows the file with these details
    name = models.CharField('Show Name', default="Slide Show Name", max_length=150)
    id = models.IntegerField('Show ID', default=0, primary_key=True)

# content models:
class File(models.Model):
    # image / file model database
    imageName = models.CharField("Image Name", max_length=250)
    file = forms.FileField()
    #uploadDate = models.DateTimeField("Upload Date") # date the file was uploaded
    expireDate = models.DateTimeField("Expire Date") # Date the file will be deleted form the system to save space
    displayTime = models.IntegerField("Display Time (Seconds)", default=15) # time to show the picture / document / etc.
    order = models.IntegerField("Special Order", default=0) # the order in which to display
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

class Page(models.Model):
    # WebPage model
    pageName = models.CharField("Page Name", max_length=200)
    pageURL = models.CharField("URL:", default="https://google.com", max_length=2000)
    startDate = models.DateTimeField("Start Date") # date to start showing
    endDate = models.DateTimeField("End Date") # date to stop showing
