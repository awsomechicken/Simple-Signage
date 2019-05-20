from django.shortcuts import render
from django.http import HttpResponse
#from django import file

# Create your views here.
def index(request):
    resp = HttpResponse("Please Hold, Development in progress...")
    return resp

def home(request):
   print("FUCK@!")
   return index(request)
