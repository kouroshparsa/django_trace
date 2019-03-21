from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
    user = models.ForeignKey(User, null=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=300)
    host = models.CharField(max_length=300)
    session = models.CharField(max_length=300)
    start = models.DateTimeField()
    info = models.TextInput(null=True, blank=True)
    duration = models.FloatField()
    status = models.PositiveIntegerField()
    def __unicode__(self):
        return str(self.start)
