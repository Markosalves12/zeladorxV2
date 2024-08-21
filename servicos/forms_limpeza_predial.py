from django import forms
from servicos.models_limpeza_predial import (ServicoLimpezaPredialAgendado, ServicoLimpezaPredialConfigurado,
                                             FatoServicoLimpezaPredial)
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial


class ServicoLimpezaPredialConfiguradoForms(forms.ModelForm):
    ServicosEscalados = forms.ModelMultipleChoiceField(
        queryset=CatalogodeServicoLimpezaPredial.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Serviços escalados',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    class Meta:
        model = ServicoLimpezaPredialConfigurado
        fields = ['area', 'ServicosEscalados', 'tempomedioplanejado', 'horario_1', 'horario_2', 'horario_3', 'horario_4', 'horario_5',
                  'horario_6', 'horario_7', 'horario_8', 'horario_9']

        labels = {
            'area': 'Área',
            'ServicosEscalados': 'Serviços Escalados',
            'tempomedioplanejado': 'Tempo médio planejado',
            'horario_1': 'Horario 1',
            'horario_2': 'Horario 2',
            'horario_3': 'Horario 3',
            'horario_4': 'Horario 4',
            'horario_5': 'Horario 5',
            'horario_6': 'Horario 6',
            'horario_7': 'Horario 7',
            'horario_8': 'Horario 8',
            'horario_9': 'Horario 9',
        }

        widgets = {
            'area': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'tempomedioplanejado': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'horario_1': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'horario_2': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'horario_3': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'horario_4': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'horario_5': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'horario_6': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'horario_7': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'horario_8': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'horario_9': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

class FatoServicoLimpezaPredialForms(forms.ModelForm):
    # def __init__(self, *args, id_random_servico=None, empresa=None, **kwargs):
    #     super(FatoServicoLimpezaPredial, self).__init__()

    class Meta:
        model = FatoServicoLimpezaPredial
        fields = ['Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area','Colaborador']

        labels = {
            'Servico': 'Serviço',
            'data_hora_chegada_na_area': 'Chegada na área',
            'data_hora_retorno_area': 'Retorno na área',
            'Colaborador': 'Colaborador'
        }

        widgets = {
            'Servico': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'data_hora_chegada_na_area': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'data_hora_retorno_area': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'Colaborador': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }