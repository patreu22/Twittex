from django.shortcuts import render
from django.views import generic
from django.conf.urls import patterns, url, include
from twittexApp import views


from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
)