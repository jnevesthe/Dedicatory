from django import forms
from .models import Dedicatory

class DedicatoryForm(forms.ModelForm):
    class Meta:
        model = Dedicatory
        fields = ['teu', 'nome', 'email', 'tipo', 'contexto', 'mensagem']
        labels = {
            'teu':'Your name',
            'nome': 'Full Name',
            'email': 'Email Address',
            'tipo': 'Type of Dedication',
            'contexto': 'Context',
            'mensagem': 'Message',
        }
        help_texts = {
            'mensagem': 'Write your dedication here, max 200 characters.',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: John Smith'}),
            'mensagem': forms.Textarea(attrs={'placeholder': 'Write your message here...', 'rows': 4}),
        }

class DedicatoryEditForm(forms.ModelForm):
    class Meta:
        model = Dedicatory
        fields = ['nome', 'email', 'tipo', 'contexto', 'mensagem', 
                  'photo1', 'photo2', 'photo3', 'photo4', 'photo5']
        labels = {
            'nome': 'Full Name',
            'email': 'Email Address',
            'tipo': 'Type of Dedication',
            'contexto': 'Context',
            'mensagem': 'Message',
            'photo1': 'Photo 1',
            'photo2': 'Photo 2',
            'photo3': 'Photo 3',
            'photo4': 'Photo 4',
            'photo5': 'Photo 5',
        }
        help_texts = {
            'mensagem': 'Write your dedication here, max 200 characters.',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: John Smith'}),
            'mensagem': forms.Textarea(attrs={'placeholder': 'Write your message here...', 'rows': 4}),
        }