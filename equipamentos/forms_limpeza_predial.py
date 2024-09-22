from django import forms
from equipamentos.models_limpeza_predial import EquipamentoDisponiveisLimpezaPredial


class EquipamentoDisponivelLimpezaPredialForm(forms.ModelForm):
    class Meta:
        model = EquipamentoDisponiveisLimpezaPredial
        fields = ['Nome', 'DataDeAquisicao', 'DataDeDesmobilizacao', 'matricula', 'EmpresaSecundaria']

        labels = {
            'Nome': 'Equipamento',
            'DataDeAquisicao': 'Data de aquisição',
            'DataDeDesmobilizacao': 'Data de desmobilização',
            'matricula': 'identificação',
            'EmpresaSecundaria': 'Empresa prestadora',
        }

        widgets = {
            'Nome': forms.TextInput(
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