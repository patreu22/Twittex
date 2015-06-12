from django.shortcuts import render
from django.views import generic
from django.conf import settings
from django.conf.urls import patterns, url, include, static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from twittexApp import views
from django.conf import settings
from django.views.generic.base import TemplateView


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^home/$', views.viewHome, name='home'),
    url(r'^profile/(?P<username>[\w-]+)/$', views.ProfileDetailView, name='profile'),
    url(r'^profile/(?P<username>[\w-]+)/edit$', views.ProfileEditView.as_view(), name='profileedit'),
    url(r'^Messages/NewMsg/$', views.NewMsgView.as_view(), name='newMsg'),
    url(r'^Messages/(?P<author>[\w-]+)/$', views.NachrichtenView.as_view(), name='messages'),
    url(r'^SendNewMsg/$', views.sendMsg, name='sendMsg'),
    url(r'^newPost/$', views.newPost, name='new_post'),
    url(r'^delete/(?P<pk>[A-Za-z0-9\w|\W]+)$', views.DeleteView.as_view(), name='delete'),
	url(r'^search/$', views.search, name='search'),
    url(r'^notification/$', views.NotificationView.as_view(), name='notifcation'),
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
    url(r'^contact/send/$', views.sendmail),
    url(r'^thanks/$', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^impressum/$', TemplateView.as_view(template_name='impressum.html'), name='impressum'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
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
