from django.contrib import admin
from .models import Log, Audit

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('url', 'start', 'user', 'method',
                    'host', 'path',
                    'duration', 'status',
                    'info', 'session')
    list_filter = ('user', 'status')
    def url(self, obj):
        return '{}{}'.format(obj.host, obj.path)

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'action')
    list_filter = ('user', 'action')

