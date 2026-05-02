from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'phone', 'email', 'address', 'notes']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'ПІБ клієнта'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+380...'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@gmail.com'
            }),

            'address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Адреса'
            }),

            'notes': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Примітки',
                'rows': 5
            }),
        }