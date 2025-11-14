from django.contrib import admin
from .models import SiteAccess

@admin.register(SiteAccess)
class SiteAccessAdmin(admin.ModelAdmin):
    list_display = ('ip', 'path', 'country', 'city', 'date', 'user_agent')
    list_filter = ('country', 'date')
    search_fields = ('ip', 'city', 'path')
