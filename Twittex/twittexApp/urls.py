from django.shortcuts import render
from django.views import generic
from django.conf.urls import patterns, url, include
from twittexApp import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        kwargs={'template_name': 'login.html'}
    ),
    url('^', include('django.contrib.auth.urls')),
)