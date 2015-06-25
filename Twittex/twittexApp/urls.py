from django.shortcuts import render
from django.views import generic
from django.conf import settings
from django.conf.urls import patterns, url, include, static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from twittexApp import views
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.views import password_reset_confirm

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^home/$', views.viewHome, name='home'),
    url(r'^profile/(?P<username>[\w-]+)/$', views.ProfileDetailView, name='profile'),
    url(r'^settings/edit$', views.ProfileEditView.as_view(), name='profileedit'),
    url(r'^Messages/NewMsg/$', views.NewMsgView.as_view(), name='newMsg'),
    url(r'^Messages/(?P<author>[\w-]+)/$', views.NachrichtenView.as_view(), name='messages'),
    url(r'^SendNewMsg/$', views.sendMsg, name='sendMsg'),
    url(r'^newPost/$', views.newPost, name='new_post'),
    url(r'^delete/(?P<pk>[A-Za-z0-9\w|\W]+)$', views.DeleteView.as_view(), name='delete'),
    url(r'^search/$', views.search, name='search'),
    url(r'^notification/$', views.viewNotification, name='notifcation'),
    url(r'^followerlist/$', views.viewList, name='list'),
    url(r'^newList/$', views.NewListView.as_view(), name='newList'),
    url(r'^followerlist/(?P<title>[\w-]+)/$', views.ListDetailView, name='detailList'),
    url(r'^followerlist/(?P<title>[\w-]+)/edit/$', views.ListEditView.as_view(), name='editList'),
    url(r'^follow/(?P<username>[\w-]+)/$', views.following, name='Follow'),
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
    url(
        r'^settings/password_change/$',
        'django.contrib.auth.views.password_change',
        kwargs={'post_change_redirect': 'twittexApp:password_change_done', 'template_name': 'password_change_form.html'}
    ),
    url(
        r'^settings/password_change_done/$',
        'django.contrib.auth.views.password_change_done',
        kwargs={'template_name': 'password_change_done.html'},
        name= 'password_change_done'
    ),
    url(
        r'^password_reset/$',
        'django.contrib.auth.views.password_reset',
        kwargs={'post_reset_redirect': 'twittexApp:password_reset_done', 'template_name': 'password_reset_form.html', 'email_template_name': 'password_reset_email.html'}
    ),
    url(
        r'^password_reset_done/$',
        'django.contrib.auth.views.password_reset_done',
        kwargs={'template_name': 'password_mail_done.html'},
        name= 'password_reset_done'
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        kwargs={'post_reset_redirect': 'twittexApp:password_reset_complete', 'template_name': 'password_reset_form.html'},
        name='password_reset_confirm'
    ),
    url(
        r'^reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        kwargs={'template_name': 'password_reset_done.html'},
        name='password_reset_complete'
    ),
    url(r'^contact/send/$', views.sendmail),
    url(r'^thanks/$', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^impressum/$', TemplateView.as_view(template_name='impressum.html'), name='impressum'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
)
