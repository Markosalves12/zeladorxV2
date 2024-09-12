from django import forms
from servicos.models_limpeza_predial import (ServicoLimpezaPredialAgendado, ServicoLimpezaPredialConfigurado,
                                             FatoServicoLimpezaPredial)
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from semana.models import DiasDaSemana
from empresasecundario.utils import define_empresa_primaria_ids


class ServicoLimpezaPredialAgendadoForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(ServicoLimpezaPredialAgendadoForms, self).__init__(*args, **kwargs)
        if userid:
            empresas_primarias_ids = define_empresa_primaria_ids(request=request, userid=userid)
            self.fields['ServicosEscalados'].queryset = self.fields['ServicosEscalados'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids
            )

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
        model = ServicoLimpezaPredialAgendado
        fields = ['area', 'DescricaoDoServico', 'ServicosEscalados', 'DataDeInicio', 'DataDeConclusao']
        labels = {
            'area': 'Área',
            'ServicosEscalados': 'Serviços Escalados',
            'DescricaoDoServico': 'Descrição do serviço',
            'DataDeInicio': 'Data marcada para inicio',
            'DataDeConclusao': 'Data prevista para conclusao',
        }

        widgets = {
            'DataDeInicio': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'DD/MM/AAAA HH:MM',
                }
            ),
            'DataDeConclusao': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'DD/MM/AAAA HH:MM',
                }
            ),
            'area': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'DescricaoDoServico': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class ServicoLimpezaPredialConfiguradoForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(ServicoLimpezaPredialConfiguradoForms, self).__init__(*args, **kwargs)
        if userid:
            empresas_primarias_ids = define_empresa_primaria_ids(request=request, userid=userid)
            self.fields['ServicosEscalados'].queryset = self.fields['ServicosEscalados'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids
            )

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

    diasaseremrealizado = forms.ModelMultipleChoiceField(
        queryset=DiasDaSemana.objects.all(),  # Usa as opções definidas no modelo
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Dias a serem realizados',
        required=True  # Defina como True se a seleção de dias for obrigatória
    )

    class Meta:
        model = ServicoLimpezaPredialConfigurado
        fields = ['area', 'ServicosEscalados', 'tempomedioplanejado', 'diasaseremrealizado','horario_1',
                  'horario_2', 'horario_3', 'horario_4', 'horario_5',
                  'horario_6', 'horario_7', 'horario_8', 'horario_9']

        labels = {
            'area': 'Área',
            'ServicosEscalados': 'Serviços Escalados',
            'tempomedioplanejado': 'Tempo médio planejado',
            'diasaseremrealizado': 'Dias a serem realizados',
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
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'horario_1': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'horario_2': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'horario_3': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'horario_4': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'horario_5': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'horario_6': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'horario_7': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'horario_8': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'horario_9': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),
        }


class FatoServicoLimpezaPredialForms(forms.ModelForm):
    # def __init__(self, *args, id_random_servico=None, empresa=None, **kwargs):
    #     super(FatoServicoLimpezaPredial, self).__init__()

    class Meta:
        model = FatoServicoLimpezaPredial
        fields = ['Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area','Gerente']

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