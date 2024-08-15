from django import forms
from equipamentos.models import EquipamentoDisponiveis


class EquipamentoDisponivelForm(forms.ModelForm):
    class Meta:
        model = EquipamentoDisponiveis
        fields = ['Nome', 'DataDeAquisicao', 'DataDeDesmobilizacao', 'matricula', 'EmpresaSecundaria']

        widgets = {
            'Nome': forms.Select(
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