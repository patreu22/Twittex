from django.conf.urls import include, url
from django.contrib import admin, auth

urlpatterns = [
    # Examples:
    # url(r'^$', 'Twittex.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('twittexApp.urls', namespace="twittexApp")),
    url(r'^admin/', include(admin.site.urls)),
]
