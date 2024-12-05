from dal import autocomplete
from django.shortcuts import render
from django.template import TemplateDoesNotExist, engines
from . import controller
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AuditView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        django_engine = engines['django']  # Django template engine
        data = controller.get_data(request)
        try:
            django_engine.get_template('base.html')
            base_exists = True
        except TemplateDoesNotExist:
            base_exists = False
        
        if base_exists:
            return render(request, 'audit_with_base.html', data)
        return render(request, 'audit.html', data)


class UsersAutocompleteView(LoginRequiredMixin,autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(Q(username__icontains=self.q)|Q(email__icontains=self.q)|Q(first_name__icontains=self.q))

        return qs