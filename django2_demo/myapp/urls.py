from django.contrib import admin
from django.urls import path
admin.autodiscover()

#urlpatterns = [
#    url(r'^admin/', include(admin.site.urls)),
#    url(r'^$', include(admin.site.urls)),
#    url(r'^main/$', 'myapp.views.main', name='main'),
#]
urlpatterns = [
    path('admin/', admin.site.urls),
    ]
