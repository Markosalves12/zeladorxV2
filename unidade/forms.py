from unidade.models import Unidade
from django import forms

class UnidadeForms(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ['nome', 'linkmapa', 'foto', 'EmpresaSecundaria', ]
        labels = {
            'nome': 'Nome',
            'linkmapa': 'Link do mapa da unidade',
            'foto': 'Fotos da unidade',
            'EmpresaSecundaria': 'Empresa operadora',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'linkmapa': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'foto': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'EmpresaSecundaria': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }