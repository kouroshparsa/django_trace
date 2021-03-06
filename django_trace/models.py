"""
This module defines the data model
"""
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.conf import settings

AUDIT = True
MAX_LEN = 300

if hasattr(settings, 'DJANGO_TRACE'):
    AUDIT = settings.DJANGO_TRACE.get('AUDIT', True)

if AUDIT:
    @receiver(user_logged_in)
    def login_callback(sender, **kwargs):
        """ trigged when the user logs in """
        user = User.objects.get(username=kwargs['user'].username)
        Audit.objects.create(user=user, action=Audit.LOGGED_IN)

    @receiver(user_logged_out)
    def logout_callback(sender, **kwargs):
        """ trigged when the user logs out """
        user = User.objects.get(username=kwargs['user'].username)
        Audit.objects.create(user=user, action=Audit.LOGGED_OUT)


class Audit(models.Model):
    """ captures any log-in/out activities """
    user = models.ForeignKey(User, null=True, blank=True,\
        on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)
    LOGGED_IN = 0
    LOGGED_OUT = 1
    ACTION_TYPES = [
        (LOGGED_IN, 'Logged in'),
        (LOGGED_OUT, 'Logged out')]
    action = models.PositiveIntegerField(choices=ACTION_TYPES)

    def __unicode__(self):
        act = 'Logged in'
        if self.action == self.LOGGED_OUT:
            act = 'Logged out'

        return u'{} {}'.format(self.user.username, act)


class Log(models.Model):
    """ captures any http requests sent """
    user = models.ForeignKey(User, null=True,\
        blank=True, on_delete=models.PROTECT)
    method = models.CharField(max_length=10)
    path = models.TextField()
    host = models.CharField(max_length=MAX_LEN)
    session = models.CharField(max_length=MAX_LEN,\
        null=True, blank=True)
    start = models.DateTimeField()
    info = models.TextField(null=True, blank=True)
    duration = models.FloatField()
    status = models.PositiveIntegerField()

    def __unicode__(self):
        return str(self.start)
