from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

from .models import *
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    if 'fail' in request.GET:
        raise Exception('Invalid code')
    return render(request, 'main.html')
