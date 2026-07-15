from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
import os

from .forms import DedicatoryForm, DedicatoryEditForm
from .models import Dedicatory


# =========================
# PÁGINAS ESTÁTICAS
# =========================

from django.views.generic import TemplateView
from .models import Dedicatory, FAQ

class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimas_dedicatorias'] = Dedicatory.objects.all()[:2]
        context['faqs_preview'] = FAQ.objects.filter(ativo=True)[:2]
        return context


class About(TemplateView):
    template_name = 'about.html'


class Privacy(TemplateView):
    template_name = 'privacy.html'


class Contact(TemplateView):
    template_name = 'contact.html'


class Terms(TemplateView):
    template_name = 'terms.html'


def dedicatories(request):
    return render(request, 'dedicatories.html')


# views.py
from django.shortcuts import render
from .models import FAQ

def faq_list(request):
    faqs = FAQ.objects.filter(ativo=True)
    return render(request, 'faq.html', {'faqs': faqs})


# =========================
# CRIAR DEDICATÓRIA
# =========================

def criar_dedicatoria(request):
    if request.method == 'POST':
        form = DedicatoryForm(request.POST, request.FILES)
        if form.is_valid():
            dedicatoria = form.save()
            return redirect('screen_dedicatory', dedicatoria.codigo)
    else:
        form = DedicatoryForm()

    return render(request, 'criar.html', {'form': form})


# =========================
# VER DEDICATÓRIA (PÚBLICA OU PRIVADA POR CÓDIGO)
# =========================

def ver_dedicatoria(request, codigo):
    dedicatory = get_object_or_404(Dedicatory, codigo=codigo)

    fotos = [
        dedicatory.photo1,
        dedicatory.photo2,
        dedicatory.photo3,
        dedicatory.photo4,
        dedicatory.photo5
    ]
    fotos = [f.url for f in fotos if f]

    templates = {
        'amor': 'amor.html',
        'carinho': 'carinho.html',
        'amizade': 'amizade.html',
        'admiracao': 'admiracao.html'
    }

    template = templates.get(dedicatory.contexto, 'galeria.html')

    return render(request, template, {
        'dedicatory': dedicatory,
        'fotos': fotos
    })


# =========================
# PESQUISA POR CÓDIGO
# =========================

def search(request):
    error = None

    if request.method == 'POST':
        codigo = request.POST.get('codigo')

        try:
            dedicatoria = Dedicatory.objects.get(codigo=codigo)
            return redirect('screen_dedicatory', codigo=dedicatoria.codigo)
        except Dedicatory.DoesNotExist:
            error = "Nenhuma dedicatória encontrada com esse código."

    return render(request, 'search.html', {'error': error})


# =========================
# CONFIRMAR PIN (EDITAR)
# =========================

def confirmar_pin_edit(request, codigo):
    dedicatoria = get_object_or_404(Dedicatory, codigo=codigo)
    erro = None

    if request.method == 'POST':
        pin = request.POST.get('pin', '').strip()

        if pin == dedicatoria.pin:
            request.session['edit_allowed'] = True
            return redirect('edit', codigo=dedicatoria.codigo)
        else:
            erro = "PIN inválido."

    return render(request, 'confirm.html', {
        'dedicatory': dedicatoria,
        'erro': erro
    })


# =========================
# CONFIRMAR PIN (DELETE)
# =========================

def confirmar_pin_delete(request, codigo):
    dedicatoria = get_object_or_404(Dedicatory, codigo=codigo)
    erro = None

    if request.method == 'POST':
        pin = request.POST.get('pin', '').strip()

        if pin == dedicatoria.pin:
            request.session['delete_allowed'] = True
            return redirect('delete', codigo=dedicatoria.codigo)
        else:
            erro = "PIN inválido."

    return render(request, 'confirm.html', {
        'dedicatory': dedicatoria,
        'erro': erro
    })


# =========================
# EDITAR DEDICATÓRIA
# =========================

class UpdateDedicatory(UpdateView):
    model = Dedicatory
    form_class = DedicatoryEditForm
    template_name = 'edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Dedicatory, codigo=self.kwargs['codigo'])

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.session.get('edit_allowed'):
            return redirect('confirm_pin_edit', codigo=obj.codigo)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session.pop('edit_allowed', None)
        return response

    def get_success_url(self):
        return reverse_lazy('screen_dedicatory', kwargs={'codigo': self.object.codigo})


# =========================
# DELETE DEDICATÓRIA
# =========================

class DeleteDedicatory(DeleteView):
    model = Dedicatory
    template_name = 'delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return get_object_or_404(Dedicatory, codigo=self.kwargs['codigo'])

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.session.get('delete_allowed'):
            return redirect('confirm_pin_delete', codigo=obj.codigo)

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        request.session.pop('delete_allowed', None)
        return response


# =========================
# SEO FILES
# =========================

def custom_404_redirect(request, exception=None):
    return render(request, '404.html', status=404)


def sitemap_view(request):
    path = os.path.join(settings.BASE_DIR, 'sitemap.xml')
    with open(path, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='application/xml')

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /confirm_edit/\n"
        "Disallow: /confirm_delete/\n"
        "Disallow: /update/\n"
        "Disallow: /delete/\n"
        "\n"
        "Sitemap: https://love-dedicatory.xyz/sitemap.xml/\n"
    )
    return HttpResponse(content, content_type="text/plain")

"""
def ads_txt_view(request):
    path = os.path.join(settings.BASE_DIR, 'ads.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='text/plain')

"""

from django.core.paginator import Paginator


TYPE_MAP = {
    'mother': 'mae',
    'father': 'pai',
    'partner': 'parceiro(a)',
    'boyfriend': 'namorado',
    'girlfriend': 'namorada',
    'sibling': 'irmao(a)',
    'friend': 'amigo(a)',
    'celebrity': 'celebridade',
    'myself': 'eu_mesmo',
}

CONTEXT_MAP = {
    'love': 'amor',
    'care': 'carinho',
    'friendship': 'amizade',
    'admiration': 'admiracao',
}

def v(request):
    context_param = request.GET.get('context')
    type_param = request.GET.get('type')

    dedicatorias = Dedicatory.objects.filter(status='publico').order_by('-criado_em')

    if context_param in CONTEXT_MAP:
        dedicatorias = dedicatorias.filter(contexto=CONTEXT_MAP[context_param])

    if type_param in TYPE_MAP:
        dedicatorias = dedicatorias.filter(tipo=TYPE_MAP[type_param])

    paginator = Paginator(dedicatorias, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'list.html', {
        'page_obj': page_obj,
        'context_filter': context_param,
        'type_filter': type_param,
    })




from django.shortcuts import redirect

def ezoic_ads_txt(request):
    # Substitua '[YOUR_DOMAIN].com' pelo seu domínio real
    ezoic_url = "https://srv.adstxtmanager.com/19390/love-dedicatory.xyz"
    return redirect(ezoic_url, permanent=True)

