from django.shortcuts import render
from django.views import generic
from django.conf.urls import patterns, url, include
from twittexApp import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^Messages/NewMsg/$', views.NewMsgView.as_view(), name='newMsg'),
    url(r'^Messages/(?P<author>[\w-]+)/$', views.NachrichtenView.as_view(), name='messages'),
    url(r'^SendNewMsg/$', views.sendMsg, name = 'sendMsg'),
    url(r'^newPost/$', views.newPost, name = 'new_post'),
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        kwargs={'template_name': 'login.html'}
    ),
	    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        kwargs={'next_page': '/','template_name': 'index.html'}
    ),
    url('^', include('django.contrib.auth.urls')),
)

"""
used urls in url('^', include('django.contrib.auth.urls'))
^login/$ [name='login']
^logout/$ [name='logout']
^password_change/$ [name='password_change']
^password_change/done/$ [name='password_change_done']
^password_reset/$ [name='password_reset']
^password_reset/done/$ [name='password_reset_done']
^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
^reset/done/$ [name='password_reset_complete']
"""
