from empresasecundario.models import EmpresaSecundaria
from django import forms

class EmpresaSecundariaForms(forms.ModelForm):
    class Meta:
        model = EmpresaSecundaria
        fields = ['nome', 'razao_social', 'CNPJ', 'logo', 'setor', 'EmpresaPrimaria', ]
        labels = {
            'nome': 'Nome',
            'razao_social': 'Razão social',
            'CNPJ': 'CNPJ (apenas os números)',
            'setor': 'Setor',
            'EmpresaSecundaria': 'Empresa operadora',
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
            'logo': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'setor': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'EmpresaPrimaria': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }