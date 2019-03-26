django_trace
==========

django_trace is a django app that monitors your web app and your server resources and audits logins and web requests
Each of these operations can be disabled and they are all secure

**How to install:**
`pip install django_trace`

**Configuration:**
- in your settings.py, under INSTALLED_APPS, add 'django_trace'
- add 'django_trace.middleware.MonitorMiddleware' to your MIDDLEWARE_CLASSES (for django<1.10) or MIDDLEWARE (for django >= 1.10)_inside your settings.py
- migrate using these commands
```
python manage.py makemigrations django_trace
python manage.py migrate
```
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
    "MEMORY_THRESHOLD": 85,
    "DISK_THRESHOLD": 85,
    "PATH_FILTER": [],
    "MAX_LOG_COUNT": 10000,
    "ONLY_TRACE_LOGGED_IN_USERS": True
    }
```

By default, ONLY_TRACE_LOGGED_IN_USERS is True which means you only record web requests for logged in users.

To see who is logged in or out of the system, see the admin page which is /admin/django_trace/audit.
To see all the http activities, see the admin page /admin/django_trace/log

If there are urls that you do not wish to monitor, you can tiler them out using a list of regex in PATH_FILTER.
By default, the system keeps 10000 records in the logs which can be modified by adjusting MAX_LOG_COUNT.

**Sending alerts when resources are running low:**

"WARNING_EMAILS" can be used to inform you when your server is running low on memory or disk usage. In order to use that, you put the emails of the people whom need to be informed in the WARNING_EMAILS list.
MEMORY_THRESHOLD and DISK_THRESHOLD have a 85% default but you can adjust them.

Then, you must run the command
```
python manage.py check_resources
```
in your cron job to check the state of your server periodically.
There is a quiet period set to 1 day so if one of the resources is running low and an email is sent, the check will abort withing the next day. If you want to change the quiet period from the default 1 day, you can use the option QUIET_TIME_MINUTES within DJANGO_TRACE.

Also, the host name is automatically determined to be included in the email. If you want to overwrite it, use the HOST option.

If you have any questions or request, please feel free to contact the author or post it on github.

