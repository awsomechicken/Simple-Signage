
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('apply_changes', views.apply_changes, name='apply changes'),
    path('upload_file', views.upload_file, name='upload file'),
    path('login',views.login, name='login'),
    path('authorize', views.loginauth, name='auth')
]
