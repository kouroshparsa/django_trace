from django.db import models
from django.contrib.auth.models import User

class Imp(models.Model):
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=20)
    content = models.TextField()
    def __unicode__(self):
        return self.name


class Int(models.Model):
    NOT_APPROVED = 0
    APPROVED = 1
    ARCHIVED = 2
    STATES = ((NOT_APPROVED, 'Not Approved'),\
        (APPROVED, 'Approved'), (ARCHIVED, 'Archived'))
    date = models.DateTimeField(auto_now=True)
    state = models.PositiveIntegerField(choices=STATES, default=0)
    def __unicode__(self):
        return str(self.id)


class Condition(models.Model):
    x = models.ForeignKey(Int, related_name='condition')
    mf = models.BooleanField(default=True)
    def __unicode__(self):
        return str(self.id)


