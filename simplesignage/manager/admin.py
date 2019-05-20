from django.contrib import admin

# Register your models here.
from .models import Show, File, Page

admin.site.register(Show)
admin.site.register(File)
