from django import forms
from empresaprimaria.models import EmpresaPrimaria

class EmpresaPrimaria(forms.Form):
    class Meta:
        model = EmpresaPrimaria
        fields = ['nome', 'razao_social', 'CNPJ', 'username', 'password', ]

        labels = {
            'nome': 'Nome de identificação na plataforma',
            'razao_social': 'Razão social',
            'CNPJ': 'CNPJ Da matriz',
            'username': 'Nome de usuário',
            'password': 'Senha de acesso'
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'razao_social': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'CNPJ': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'password': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }