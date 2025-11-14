from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import TemplateView
from .forms import DedicatoryForm, DedicatoryEditForm
from .models import Dedicatory

class Home(TemplateView):
    template_name= 'index.html'
    
    
class About(TemplateView):
    template_name= 'about.html'
    
    
class Privacy(TemplateView):
    template_name= 'privacy.html'  
    
class Contact(TemplateView):
    template_name= 'contact.html'     
    
class Terms(TemplateView):
    template_name= 'terms.html'          

def criar_dedicatoria(request):
    if request.method == 'POST':
        form = DedicatoryForm(request.POST, request.FILES)
        if form.is_valid():
            dedicatoria = form.save()
            return redirect('screen_dedicatory', dedicatoria.codigo)
             
    else:
        form = DedicatoryForm()
    return render(request, 'criar.html', {'form': form})


def ver_dedicatoria(request, codigo):
    dedicatory = get_object_or_404(Dedicatory, codigo=codigo)
    fotos = [dedicatory.photo1, dedicatory.photo2, dedicatory.photo3, dedicatory.photo4, dedicatory.photo5]
    fotos = [foto.url for foto in fotos if foto]  # só as que existem

    # Escolhe o HTML conforme o contexto
    if dedicatory.contexto == 'amor':
        template = 'amor.html'
    elif dedicatory.contexto == 'carinho':
        template = 'carinho.html'
    elif dedicatory.contexto == 'amizade':
        template = 'amizade.html'
    else:
        template = 'galeria.html'  # fallback padrão

    return render(request, template, {'dedicatory': dedicatory, 'fotos': fotos})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Dedicatory

def search(request):
    dedicatory = None
    codigo = None
    error = None

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        try:
            dedicatory = Dedicatory.objects.get(codigo=codigo)
            # Se encontrado, redireciona para a página da dedicatória
            return redirect('screen_dedicatory', codigo=dedicatory.codigo)
        except Dedicatory.DoesNotExist:
            error = f'No dedication found with the code "{codigo}".'

    return render(request, 'search.html', {'error': error, 'codigo': codigo})

def confirmar_email_edit(request, codigo):
    """
    Verifica se o e-mail informado corresponde ao e-mail da dedicatória com o código fornecido.
    """
    dedicatoria = get_object_or_404(Dedicatory, codigo=codigo)
    erro = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if email == dedicatoria.email:
            # Cria sessão permitindo editar
            request.session['editar'] = True
            request.session['email'] = email
            return redirect('edit', codigo=dedicatoria.codigo)
        else:
            erro = "O e-mail não corresponde à dedicatória informada."

    return render(request, 'confirm.html', {'dedicatory': dedicatoria, 'erro': erro})
    
def confirmar_email_delete(request, codigo):
    """
    Verifica se o e-mail informado corresponde ao e-mail da dedicatória com o código fornecido.
    """
    dedicatoria = get_object_or_404(Dedicatory, codigo=codigo)
    erro = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if email == dedicatoria.email:
            # Cria sessão permitindo editar
            request.session['delete'] = True
            request.session['email'] = email
            return redirect('delete', codigo=dedicatoria.codigo)
        else:
            erro = "O e-mail não corresponde à dedicatória informada."

    return render(request, 'confirm.html', {'dedicatory': dedicatoria, 'erro': erro})
 
    
"""          
class UpdateDedicatory(UpdateView):
   
    Segunda etapa: editar a dedicatória, se o e-mail da sessão for o mesmo do banco.
    model = Dedicatory
    form_class = DedicatoryEditForm
    template_name = 'edit.html'

    def dispatch(self, request, *args, **kwargs):
        codigo = kwargs.get('codigo')
        dedicatoria = get_object_or_404(Dedicatory, codigo=codigo)

        # Verifica se há permissão de edição na sessão
        email_sessao = request.session.get('email')
        editar_sessao = request.session.get('editar')

        if not editar_sessao or not email_sessao:
            return redirect('confirmar_email', codigo=codigo)

        # Confirma que o e-mail da sessão é o mesmo do banco
        if dedicatoria.email != email_sessao:
            # Se não for igual, limpa a sessão e redireciona
            request.session.pop('editar', None)
            request.session.pop('email', None)
            return redirect('confirmar_email', codigo=codigo)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        # Após salvar, remove as variáveis da sessão
        self.request.session.pop('editar', None)
        self.request.session.pop('email', None)
        return response

    def get_success_url(self):
        return reverse_lazy('screen_dedicatory', kwargs={'codigo': self.object.codigo})
        
""" 

class UpdateDedicatory(UpdateView):
    """
    Segunda etapa: editar a dedicatória, se o e-mail da sessão for o mesmo do banco.
    """
    model = Dedicatory
    form_class = DedicatoryEditForm
    template_name = 'edit.html'

    # Sobrescreve get_object para usar codigo em vez de pk
    def get_object(self, queryset=None):
        codigo = self.kwargs.get('codigo')
        return get_object_or_404(Dedicatory, codigo=codigo)

    def dispatch(self, request, *args, **kwargs):
        dedicatoria = self.get_object()  # agora pega pelo get_object

        # Verifica se há permissão de edição na sessão
        email_sessao = request.session.get('email')
        editar_sessao = request.session.get('editar')

        if not editar_sessao or not email_sessao:
            return redirect('confirm_edit', codigo=dedicatoria.codigo)

        # Confirma que o e-mail da sessão é o mesmo do banco
        if dedicatoria.email != email_sessao:
            # Se não for igual, limpa a sessão e redireciona
            request.session.pop('editar', None)
            request.session.pop('email', None)
            return redirect('confirm_edit', codigo=dedicatoria.codigo)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        # Após salvar, remove as variáveis da sessão
        self.request.session.pop('editar', None)
        self.request.session.pop('email', None)
        return response

    def get_success_url(self):
        return reverse_lazy('screen_dedicatory', kwargs={'codigo': self.object.codigo})              



class DeleteDedicatory(DeleteView):
    model = Dedicatory
    template_name = 'delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        codigo = self.kwargs.get('codigo')
        return get_object_or_404(Dedicatory, codigo=codigo)

    def dispatch(self, request, *args, **kwargs):
        self.dedicatoria = self.get_object()

        # Sempre verificar sessão
        email_sessao = request.session.get('email')
        delete_sessao = request.session.get('delete')

        # --- VERIFICAÇÃO DE SEGURANÇA ---
        if not delete_sessao or not email_sessao:
            return redirect('confirm_delete', codigo=self.dedicatoria.codigo)

        if self.dedicatoria.email != email_sessao:
            return redirect('confirm_delete', codigo=self.dedicatoria.codigo)

        # --- APAGAR SESSÃO APENAS NO POST ---
        if request.method == "POST":
            request.session.pop('email', None)
            request.session.pop('delete', None)

        return super().dispatch(request, *args, **kwargs)
    

# views.py
from django.shortcuts import render

def custom_404_redirect(request, exception=None):
    # redireciona para uma p��gina espec��fica
    return render(request, '404.html', status=404)

               