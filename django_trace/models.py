from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.conf import settings

AUDIT = True
if hasattr(settings, 'DJANGO_TRACE'):
    AUDIT = settings.DJANGO_TRACE.get('AUDIT', True)

if AUDIT:
    @receiver(user_logged_in)
    def login_callback(sender, **kwargs):
        user = User.objects.get(username=kwargs['user'].username)
        Audit.objects.create(user=user, action=Audit.LOGGED_IN)

    @receiver(user_logged_out)
    def login_callback(sender, **kwargs):
        user = User.objects.get(username=kwargs['user'].username)
        Audit.objects.create(user=user, action=Audit.LOGGED_OUT)

class Audit(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    LOGGED_IN = 0
    LOGGED_OUT = 1
    ACTION_TYPES = [(LOGGED_IN, 'Logged in'), (LOGGED_OUT, 'Logged out')]
    action = models.PositiveIntegerField(choices=ACTION_TYPES)
    def __unicode__(self):
        act = 'Logged in'
        if self.action == LOGGED_OUT:
            act = 'Logged out'
        return unicode(self.user.username, act)

class Log(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=300)
    host = models.CharField(max_length=300)
    session = models.CharField(max_length=300, null=True, blank=True)
    start = models.DateTimeField()
    info = models.TextField(null=True, blank=True)
    duration = models.FloatField()
    status = models.PositiveIntegerField()
    def __unicode__(self):
        return str(self.start)
