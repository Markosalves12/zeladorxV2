from django import forms
from manutencao.models import MotivoDaManutencao, ManutencaoDeEquipamentos, CatalogoManutencao


class CatalogoManutencaoForms(forms.ModelForm):
    class Meta:
        model = CatalogoManutencao
        fields = ['nome', 'EmpresaSecundaria']
        labels = {
            'nome': 'Tipo de manutenção',
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




class MotivoDaManutencaoForms(forms.ModelForm):
    class Meta:
        model = MotivoDaManutencao
        fields = ['nome', 'EmpresaSecundaria', ]
        labels = {
            'nome': 'Motivo da manutenção',
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


class ManutencaoDeEquipamentosForms(forms.ModelForm):
    class Meta:
        model = ManutencaoDeEquipamentos
        fields = ['Equipamento', 'DataDeInicio', 'DataFim', 'CatalogoManutencao', 'MotivoManutencao', 'Descricaodoservico', ]
        labels = {
            'Equipamento': 'Equipamento',
            'DataDeInicio': 'Data e hora de envio para a manutenção',
            'DataFim': 'Data e hora de retorno da manutenção',
            'CatalogoManutencao': 'Tipo de manutenção aplicada',
            'MotivoManutencao': 'Motivo da manutenção',
            'Descricaodoservico': 'Descrição do serviço',
        }

        widgets = {
            'Equipamento': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'DataDeInicio': forms.DateTimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'DataFim': forms.DateTimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'CatalogoManutencao': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'MotivoManutencao': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'Descricaodoservico': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
