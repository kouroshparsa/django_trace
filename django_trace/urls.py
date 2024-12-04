from django.urls import path
from django_trace.trace_views import AuditView, UsersAutocompleteView

app_name = "django_trace"

urlpatterns = [
    path('', AuditView.as_view(), name='audit'),
    path('users_autocompletion', UsersAutocompleteView.as_view(), name='users_autocompletion'),
]
