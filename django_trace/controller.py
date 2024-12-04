from .models import Log
from django.core.paginator import Paginator


def get_data(request):
    filter_session = request.GET.get('filter_session', '')
    filter_user = request.GET.get('filter_user', '')
    queryset = Log.objects.all()
    if filter_session:
        queryset = queryset.filter(session=filter_session)

    if filter_user:
        queryset = queryset.filter(user=filter_user)
 
    paginator = Paginator(queryset, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'logs': page_obj.object_list,
        'page_obj': page_obj,
    }
    return context