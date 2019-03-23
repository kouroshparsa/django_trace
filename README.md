django_trace
==========

django_trace is a django app that monitors your web app and your server resources and audits logins and web requests
Each of these operations can be disabled and they are all secure

**How to install:**
`pip install django_trace`

**Configuration:**
- in your settings.py, under INSTALLED_APPS, add 'django_trace'
- optionally you can configure the options for django_trace by adding DJANGO_TRACE to your settings.py.

Here is an optional configuration that you can put in your settings.py
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreply@mycompany.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DJANGO_TRACE = {
    "WARNING_EMAILS": ["me@mycompany.com"],
    "MEMORY_THRESHOLD": 90,
    "DISK_THRESHOLD": 90,
    "PATH_FILTER": [],
    "MAX_LOG_COUNT": 10000,
    "ONLY_TRACE_LOGGED_IN_USERS": False
    }
```

By default, ONLY_TRACE_LOGGED_IN_USERS is True which means you only record web requests for logged in users.

To see who is logged in or out of the system, see the admin page which is /admin/django_trace/audit.
To see all the http activities, see the admin page /admin/django_trace/log

If there are urls that you do not wish to monitor, you can tiler them out using a list of regex in PATH_FILTER.
By default, the system keeps 10000 records in the logs which can be modified by adjusting MAX_LOG_COUNT.

**Sending alerts when resources are running low:**

"WARNING_EMAILS" can be used to inform you when your server is running low on memory or disk usage. In order to use that, you
need to specify either or both MEMORY_THRESHOLD and DISK_THRESHOLD which are percent usage threshold. Exceeding these values t
riggers the emails.
You must run the command
```
python manage.py check_resources
```
in your cron job.

