from django import forms
from gerente.models import Gerente

class GerenteForms(forms.ModelForm):
    class Meta:
        model = Gerente
        fields = ['username', 'email', 'funcao']
        labels = {
            'username': 'Nome do gerente',
            'email': 'Email de contato',
            'funcao': 'Função principal',
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
        }