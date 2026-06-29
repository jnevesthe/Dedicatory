from django import forms
from .models import Dedicatory
from django.forms.widgets import ClearableFileInput


# =========================
# FORM DE CRIAÇÃO
# =========================
class DedicatoryForm(forms.ModelForm):
    class Meta:
        model = Dedicatory
        fields = [
            'teu',
            'nome',
            'pin',
            'tipo',
            'contexto',
            'status',
            'mensagem'
        ]

        labels = {
            'teu': 'Your Name',
            'nome': 'Full Name',
            'pin': '4 digits Pin',
            'tipo': 'Type of Dedication',
            'contexto': 'Context',
            'status': 'Visibility',
            'mensagem': 'Message',
        }

        help_texts = {
            'mensagem': 'Write your dedication here.',
            'status': 'Public = everyone can see, Private = needs code.',
        }

        widgets = {
            'teu': forms.TextInput(attrs={'placeholder': 'Ex: João'}),
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Maria Silva'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
            'tipo': forms.Select(),
            'contexto': forms.Select(),
            'status': forms.Select(),

            'mensagem': forms.Textarea(attrs={
                'placeholder': 'Write your message here...',
                'rows': 4
            }),
        }


# =========================
# FORM DE EDIÇÃO
# =========================
class DedicatoryEditForm(forms.ModelForm):
    class Meta:
        model = Dedicatory
        fields = [
            'teu',
            'nome',
            'pin',
            'tipo',
            'contexto',
            'status',
            'mensagem',
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'photo5'
        ]

        labels = {
            'teu': 'Your Name',
            'nome': 'Full Name',
            'email': 'Email Address',
            'tipo': 'Type of Dedication',
            'contexto': 'Context',
            'status': 'Visibility',
            'mensagem': 'Message',
            'photo1': 'Photo 1',
            'photo2': 'Photo 2',
            'photo3': 'Photo 3',
            'photo4': 'Photo 4',
            'photo5': 'Photo 5',
        }

        widgets = {
            'teu': forms.TextInput(attrs={'placeholder': 'Ex: João'}),
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Maria Silva'}),
            'pin': forms.TextInput(attrs={'placeholder': '4-digit PIN'}),

            'tipo': forms.Select(),
            'contexto': forms.Select(),
            'status': forms.Select(),

            'mensagem': forms.Textarea(attrs={
                'placeholder': 'Write your message here...',
                'rows': 4
            }),

            'photo1': ClearableFileInput(attrs={'input_text': 'Choose file'}),
            'photo2': ClearableFileInput(attrs={'input_text': 'Choose file'}),
            'photo3': ClearableFileInput(attrs={'input_text': 'Choose file'}),
            'photo4': ClearableFileInput(attrs={'input_text': 'Choose file'}),
            'photo5': ClearableFileInput(attrs={'input_text': 'Choose file'}),
        }
