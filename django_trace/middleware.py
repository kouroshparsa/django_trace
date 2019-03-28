import re
from .models import Log
from django.contrib.auth.models import User
from django.conf import settings
import pytz
from django.utils import timezone
from django import http
import traceback

ONLY_TRACE_LOGGED_IN_USERS = True
PATH_FILTER = []
MAX_LOG_COUNT = 10000

if hasattr(settings, 'DJANGO_TRACE'):
    ONLY_TRACE_LOGGED_IN_USERS = settings.DJANGO_TRACE.get('ONLY_TRACE_LOGGED_IN_USERS', ONLY_TRACE_LOGGED_IN_USERS)
    PATH_FILTER = settings.DJANGO_TRACE.get('PATH_FILTER', PATH_FILTER)
    MAX_LOG_COUNT = settings.DJANGO_TRACE.get('MAX_LOG_COUNT', MAX_LOG_COUNT)

def pass_filter(path):
    """
    path: is the url context without the host, like /admin/
    returns a boolean
    """
    if path in ['/admin/django_trace/log/', '/admin/jsi18n/']:
        return False

    for val in PATH_FILTER:
        if re.match(val, path):
            return False
    return True


class MonitorMiddleware(object):
    # django >= 1.10:
    def __init__(self, get_response=None):
        # set to None because django 1.8 does not take a second parameter
        self.get_response = get_response

    def __call__(self, request):
        self.start_t = timezone.now()
        response = self.get_response(request)
        return self.process_response(request, response)

    # django 1.8 and 1.9:
    def process_exception(self, request, exception):
        self.error = traceback.format_exc()

    def process_request(self, request):
        self.start_t = timezone.now()

    def process_response(self, request, response):
        self.end_t = timezone.now()
        if not hasattr(self, 'start_t'):
            print('No start_t')
            self.start_t = self.end_t
        duration = (self.end_t - self.start_t).total_seconds()

        info = None
        if request.method=='POST':
            if '_save' in request.POST:
                info = 'save'
            elif 'action' in request.POST and\
                'delete_selected' in request.POST and\
                'post' in request.POST and\
                request.POST['post'] == ['yes']:
                info = 'delete'

        if response.status_code == 500 and hasattr(self, 'error'):
            # typically process_exception is called but if there is a setup problem
            # it will not be called
            info = self.error


        if pass_filter(request.get_full_path()):
            user = None
            if hasattr(request, 'user'):
                if isinstance(request.user.is_anonymous, bool): # django >= 1.10
                    if not request.user.is_anonymous:
                        user = request.user
                else: # otherwise, for django 1.8 is_anonymous is a method:
                    if not request.user.is_anonymous():
                        user = request.user

            if user is None and ONLY_TRACE_LOGGED_IN_USERS:
                return response

            session = None
            if request.session is not None:
                session = request.session.session_key

            Log.objects.create(method=request.method,
                path=request.get_full_path(), host=request.get_host(),
                start=self.start_t, user=user, info=info, status=response.status_code,
                duration=duration, session=session)

            if Log.objects.all().count() > MAX_LOG_COUNT:
                Log.objects.earliest('start').delete()

        return response
