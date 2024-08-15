from django import forms
from ferramentas.models import CatalogoDeFerramentas, FerramentasDisponiveis


class CatalogoFerramentaForms(forms.Form):
    class Meta:
        model = CatalogoDeFerramentas
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


class EquipamentoDisponivelForm(forms.Form):
    class Meta:
        model = FerramentasDisponiveis
        fields = ['Nome', 'DataDeAquisicao', 'DataDeDesmobilizacao', 'matricula', 'EmpresaSecundaria']

        widgets = {
            'nome': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'DataDeAquisicao': forms.DateInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'DataDeDesmobilizacao': forms.DateInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'matricula': forms.TextInput(
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