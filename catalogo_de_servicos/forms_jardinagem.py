from django import forms
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem

class CatalogoServicoJardinagemForms(forms.ModelForm):
    class Meta:
        model = CatalogodeServicoJardinagem
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