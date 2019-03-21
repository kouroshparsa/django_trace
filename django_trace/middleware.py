import sys
from datetime import datetime
from webint.models import Log
from django.contrib.auth.models import User
from webint.settings import TIME_ZONE
import pytz
from django.utils import timezone
from django import http
import traceback

class MonitorMiddleware(object):
    def process_exception(self, request, exception):
        self.error = traceback.format_exc()

    def process_request(self, request):
        self.start_t = timezone.now()

    def process_response(self, request, response):
        self.end_t = timezone.now()
        if not hasattr(self, 'start_t'):
            print 'No start_t'
            self.start_t = self.end_t
        duration = (self.end_t - self.start_t).total_seconds()

        info = None
        if request.method=='POST':
            if '_save' in request.POST:
                info = 'save'

        if response.status_code == 500:
            info = self.error


        if request.get_full_path() not in ['/admin/webint/log/', '/admin/jsi18n/']:
            user = None
            if hasattr(request, 'user') and not request.user.is_anonymous():
                user = request.user
        
            Log.objects.create(method=request.method,
                path=request.get_full_path(), host=request.get_host(),
                start=self.start_t, user=user, info=info, status=response.status_code,
                duration=duration, session=request.session.session_key)
        return response
