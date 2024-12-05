from .models import Log
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib.auth.models import User


def get_data(request):
    filter_session = request.GET.get('filter_session', '')
    filter_user = request.GET.get('filter_user', '')
    filter_user_name = ''
    filter_date_from = request.GET.get('filter_date_from', '')
    filter_date_to = request.GET.get('filter_date_to', '')
    queryset = Log.objects.all()
    if filter_session:
        queryset = queryset.filter(session=filter_session)

    if filter_user:
        queryset = queryset.filter(user=filter_user)
        filter_user_name = User.objects.filter(id=filter_user)[0].username

    if filter_date_from:
        naive_datetime = datetime.strptime(filter_date_from, '%Y-%m-%dT%H:%M')
        queryset = queryset.filter(start__gte=naive_datetime)
    
    if filter_date_to:
        naive_datetime = datetime.strptime(filter_date_to, '%Y-%m-%dT%H:%M')
        queryset = queryset.filter(start__lte=naive_datetime)
    
    queryset = queryset.order_by('-start')
    paginator = Paginator(queryset, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter_user': filter_user,
        'filter_user_name': filter_user_name,
        'logs': page_obj.object_list,
        'page_obj': page_obj,
    }
    return context