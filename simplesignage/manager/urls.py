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
    path('deletecontent',views.delete_content, name='delete content'),
    path('makevideo', views.make_video, name='Make Video'),
    path('video_compile_status_request', views.video_compile_status, name='request status'),
    path('screens', views.screens, name='Screen Settings'),
    path('newscreen', views.newScreen, name='New Screen'),
    path('deletescreen', views.deleteScreen, name='Delete Screen'),
    path('documentation', views.documentation, name='Documentaion'),
    path('tv_check_for_new_content', views.check_new_video, name='New Content Check'),
    path('tv_get_new_content', views.get_tv_video, name='New Content Get'),
    # Authentication forms... don't forget the quotes dipshit...
    path('accounts/', include('django.contrib.auth.urls'))
]
