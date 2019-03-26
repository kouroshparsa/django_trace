"""
This module sends notifications when resources are running low
"""
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from django_trace.models import Audit, Log
from django.core.mail import send_mail
import logging
import psutil
import socket
import subprocess
from django.core.cache import cache

logger = logging.getLogger(__name__)
KEY = 'DJANGO_TRACE_SENT_EMAIL'
QUIET_TIME_MINUTES = 24 * 60
if hasattr(settings, 'DJANGO_TRACE'):
    QUIET_TIME_MINUTES = settings.DJANGO_TRACE.get(QUIET_TIME_MINUTES, QUIET_TIME_MINUTES)

def memory_check():
    """
    Example: 90 threshold
    if 95% memory is used, specified users will receive a warning email
    """
    if not hasattr(settings, 'DJANGO_TRACE'):
        logger.warn('No DJANGO_TRACE specified in the settings')
        return

    threshold = settings.DJANGO_TRACE.get('MEMORY_THRESHOLD', None)
    if threshold is None:
        return

    emails = settings.DJANGO_TRACE.get('WARNING_EMAILS', [])
    if len(emails) < 1:
        logger.warn('No emails specified in DJANGO_TRACE["WARNING_EMAILS"]')
        return

    if psutil.virtual_memory().percent > threshold:
        host = settings.DJANGO_TRACE.get('HOST', socket.gethostname())
        logger.info('Sending emails regarding lack of memory.')
        send_mail('Lack of Memory', 'The server {} is running low in memory.'.format(host),\
            '', emails)
        cache.set(KEY, True, QUIET_TIME_MINUTES * 60)


def get_used_disk_space():
    df = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE)
    output, err = df.communicate()
    ind = re.sub(r' +', ' ', output.splitlines()[0]).split(' ').index('Use%')
    if ind < 0:
        ind = 4
    used = re.sub(r' +', ' ', output.splitlines()[1]).split(' ')[ind].replace("%", "")
    return float(used)


def disk_check():
    """
    Example: 90 threshold
    if 95% memory is used, specified users will receive a warning email
    """
    if not hasattr(settings, 'DJANGO_TRACE'):
        logger.warn('No DJANGO_TRACE specified in the settings')
        return

    threshold = settings.DJANGO_TRACE.get('DISK_THRESHOLD', None)
    if threshold is None:
        return

    emails = settings.DJANGO_TRACE.get('WARNING_EMAILS', [])
    if len(emails) < 1:
        logger.warn('No emails specified in DJANGO_TRACE["WARNING_EMAILS"]')
        return

    if get_used_disk_space() > threshold:
        host = settings.DJANGO_TRACE.get('HOST', socket.gethostname())
        logger.info('Sending emails regarding lack of disk space.')
        send_mail('Lack of disk space', 'The server {} is running low in disk space.'.format(host),\
            '', emails)
        cache.set(KEY, True, QUIET_TIME_MINUTES * 60)


class Command(BaseCommand):
    """ checks the memory usage and emails notifications """
    def handle(self, *args, **options):
        if cache.get(KEY) is not None:
            logging.info('Recently sent and email so will not be checking again.')
            return

        memory_check()
        disk_check()


