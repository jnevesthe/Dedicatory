from django.contrib import admin
from .models import Dedicatory

admin.site.register(Dedicatory)

# admin.py

from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'ordem', 'ativo')
    list_editable = ('ordem', 'ativo')
    search_fields = ('pergunta',)
