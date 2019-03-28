from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'myapp.views.home', name='home'),
    url(r'^main/', 'myapp.views.main'),
    url(r'^admin/', include(admin.site.urls)),
]
