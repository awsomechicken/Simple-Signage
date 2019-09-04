from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf.urls import url
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('apply_changes', views.apply_changes, name='apply changes'),
    path('upload_file', views.upload_file, name='upload file'),
    path('delete',views.delete_content, name='delete content'),
    path('makevideo', views.make_video, name='Make Video'),
    path('screens', views.screens, name='Screen Settings'),
    path('newscreen', views.newScreen, name='New Screen'),
    path('deletescreen', views.deleteScreen, name='Delete Screen'),
    # Authentication forms... don't forget the quotes dipshit...
    path('accounts/', include('django.contrib.auth.urls'))
]
