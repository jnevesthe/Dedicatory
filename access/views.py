from django.shortcuts import render
from django.views.generic import TemplateView


class Index(TemplateView):

    template_name='index.html'


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import SiteAccess


@staff_member_required
def limpar_acessos(request):
    total, _ = SiteAccess.objects.all().delete()
    messages.success(request, f"{total} acessos apagados com sucesso.")
    return redirect('/admin/access/siteaccess/')
