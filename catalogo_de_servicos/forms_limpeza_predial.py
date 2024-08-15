from django.forms import forms
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial

class CatalogoServicoLimpezaPredialForms(forms.ModelForm):
    class Meta:
        model = CatalogodeServicoLimpezaPredial
        fields = ['nome', 'EmpresaSecundaria', ]

        labels = {
            'nome': 'Nome do serviço',
            'EmpresaSecundaria': 'Empresa prestadora',
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
