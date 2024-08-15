from django import forms
from colaborador.models import Colaborador

class ColaboradorForms(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['username', 'email', 'funcao', 'atividades', 'gerente', ]

        labels = {
            'username': 'Nome do colaborador',
            'email': 'Email de contado (opcional)',
            'funcao': 'Função principal',
            'atividades': 'Atividades principais',
            'gerente': 'Gerente imediato'
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
            'atividades': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'gerente': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }