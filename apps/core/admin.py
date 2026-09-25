from django.contrib import admin
from .models import ProspectorProfile


@admin.register(ProspectorProfile)
class ProspectorProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'xp', 'cash_earned', 'conversion_rate', 'total_doors_knocked', 'total_sales')
    search_fields = ('name',)
