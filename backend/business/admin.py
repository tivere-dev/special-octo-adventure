from django.contrib import admin
from .models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'user', 'currency', 'created_at']
    list_filter = ['currency', 'created_at']
    search_fields = ['business_name', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
