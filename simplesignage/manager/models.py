from django.db import models
from django import forms

# Create your models here.
# modles define feilds and tables.

# content models:
class File(models.Model):
    # image / file model database
    imageName = models.CharField(max_length=250)
    file = forms.FileField()
    uploadDate = models.DateTimeField("Upload Date") # date the file was uploaded
    expireDate = models.DateTimeField("Expire Date") # Date the file will be deleted form the system to save space

class Page(models.Model):
    # WebPage model
    pageName = models.CharField(max_length=2000)
    startDate = models.DateTimeField("Start Date") # date to start showing
    endDate = models.DateTimeField("End Date") # date to stop showing



# shows and presentation models
class Show(models.Model):
    # slide show model, shows the file with these details
    image = models.ForeignKey(File, on_delete=models.CASCADE)
    displayTime = models.IntegerField(default=15) # time to show the picture / document / etc.
    order = models.IntegerField(default=0) # the order in which to display
