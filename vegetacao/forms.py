from django import forms
from vegetacao.models import CatalogoVegetacao

class CatalogoVegetacaoForm(forms.ModelForm):
    class Meta:
        model = CatalogoVegetacao
        fields = ['nome', 'EmpresaSecundaria', ]
        labels = {
            'nome': 'Vegetação',
            'EmpresaSecundaria': 'Empresa operadora',
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
            ),
        }