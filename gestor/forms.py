from django import forms
from gestor.models import Gestor


class GestorForms(forms.ModelForm):
    class Meta:
        model = Gestor
        fields = ['username', 'email', 'funcao', 'EmpresaSecundaria']
        labels = {
            'username': 'Nome do gestor',
            'email': 'Email de contato',
            'funcao': 'Função principal',
            'EmpresaSecundaria': 'Empresa',
        }

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'funcao': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'EmpresaSecundaria': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }