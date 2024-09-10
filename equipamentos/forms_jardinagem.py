from django import forms
from equipamentos.models_jardinagem import EquipamentoDisponiveisJardinagem


class EquipamentoDisponivelJardinagemForm(forms.ModelForm):
    class Meta:
        model = EquipamentoDisponiveisJardinagem
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