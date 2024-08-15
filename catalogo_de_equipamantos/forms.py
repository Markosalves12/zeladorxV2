from django import forms
from catalogo_de_equipamantos.models import CatalogoDeEquipamentos


class CatalogoEquipamentoForms(forms.ModelForm):
    class Meta:
        model = CatalogoDeEquipamentos
        fields = ['nome', 'EmpresaSecundaria']
        labels = {
            'nome': 'Nome do equipamento',
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