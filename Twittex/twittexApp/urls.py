from django.shortcuts import render
from django.views import generic
from django.conf.urls import patterns, url
from twittexApp import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
)