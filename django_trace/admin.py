from django.contrib import admin
from .models import Log, Audit
from django.utils.html import mark_safe

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('url', 'start', 'user', 'method',
                    'host', '_path',
                    'duration', 'status',
                    'info', '_session')
    list_filter = ('user', 'status')
    search_fields = ('path',)

    def _path(self, obj):
        return mark_safe('<a href="/admin/django_trace'\
            '/log/?path={}">{}</a>'.format(obj.path, obj.path))

    def _session(self, obj):
        return mark_safe('<a href="/admin/django_trace'\
            '/log/?session={}">{}</a>'.format(obj.session, obj.session))

    def url(self, obj):
        return '{}{}'.format(obj.host, obj.path)

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'action')
    list_filter = ('user', 'action')

