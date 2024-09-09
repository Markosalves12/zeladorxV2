from django import forms
from catalogo_de_equipamantos.models_limpeza_predial import CatalogoDeEquipamentosLimpezaPredial


class CatalogoEquipamentoFormsLimpezaPredial(forms.ModelForm):
    class Meta:
        model = CatalogoDeEquipamentosLimpezaPredial
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