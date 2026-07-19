from django.contrib import admin
from .models import Dedicatory, FAQ


@admin.register(Dedicatory)
class DedicatoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    list_display = ('nome', 'teu', 'status', 'codigo', 'slug', 'criado_em')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('pergunta',)}
    list_display = ('pergunta', 'slug', 'ordem', 'ativo')
