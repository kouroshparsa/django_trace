from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('url', 'start', 'user', 'method',
                    'host', 'path',
                    'duration', 'status',
                    'info', 'session')
    list_filter = ('user', 'status')
    def url(self, obj):
        return '{}{}'.format(obj.host, obj.path)
