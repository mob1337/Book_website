from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [

path('homepage.html',views.home),
path('',views.home),
path('register.html',views.register),
path('login.html', views.login),
path('logout',views.logout),
path('media.html',views.media),
path('search.html',views.search),
path('media_offline.html',views.media_offline)

]
