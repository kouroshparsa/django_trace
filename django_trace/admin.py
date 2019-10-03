from django.contrib import admin
from .models import Log, Audit
from django.utils.html import mark_safe


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('start', 'user', 'method',
                    'host',
                    'duration', 'status',
                    'info', '_session', '_path')
    list_filter = ('user', 'status', 'method')
    search_fields = ('path',)

    def _path(self, obj):
        return mark_safe('<a href="/admin/django_trace'\
            '/log/?path={}">{}</a>'.format(obj.path, obj.path[:40]))

    def _session(self, obj):
        return mark_safe('<a href="/admin/django_trace'\
            '/log/?session={}">{}</a>'.format(obj.session, obj.session))

    def url(self, obj):
        return '{}{}'.format(obj.host, obj.path)


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'action')
    list_filter = ('user', 'action')

