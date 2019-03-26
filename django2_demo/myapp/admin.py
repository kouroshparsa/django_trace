from django.contrib import admin
from django.conf.urls import url
from .models import *
from .forms import *
import time

@admin.register(Imp)
class ImpAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'content')
    search_fields = ('content',)

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('id',)

class ConditionInlineAdmin(admin.TabularInline):
    form = ConditionForm
    model = Condition
    extra = 0

@admin.register(Int)
class IntAdmin(admin.ModelAdmin):
    inlines = [ConditionInlineAdmin,]
    list_display = ('id', 'date', 'state')
    def get_queryset(self, request):
        time.sleep(4) # add a delay for testing
        return super(IntAdmin, self).get_queryset(request)


