from terrenos.models import Terreno
from django import forms

class TerrenoForms(forms.ModelForm):
    class Meta:
        model = Terreno
        fields = ['nome', 'EmpresaSecundaria', ]
        labels = {
            'nome': 'Nome do terreno',
            'EmpresaSecundaria': 'Empresa operadora'
        }

        widgets = {
            'nome': forms.TextInput(
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

