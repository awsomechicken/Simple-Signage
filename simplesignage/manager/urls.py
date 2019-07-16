from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf.urls import url
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    #path('home', views.home, name='home'),
    path('apply_changes', views.apply_changes, name='apply changes'),
    path('upload_file', views.upload_file, name='upload file'),
    #path('login',views.login, name='login'),
    #path('authorize', views.loginauth, name='auth'),
    # Authentication forms... don't forget the quotes dipshit...
    path('accounts/', include('django.contrib.auth.urls'))
]
