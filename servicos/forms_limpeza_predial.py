from django import forms
from servicos.models_limpeza_predial import (ServicoLimpezaPredialAgendado, ServicoLimpezaPredialConfigurado,
                                             FatoServicoLimpezaPredial)
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from semana.models import DiasDaSemana
from empresasecundario.utils import define_empresas


class ServicoLimpezaPredialAgendadoForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(ServicoLimpezaPredialAgendadoForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type=='creat/edit':
            self.fields['ServicosEscalados'].queryset = self.fields['ServicosEscalados'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                EmpresaSecundaria__status__in=['Mobilizado'],
                status__in=['Mobilizado']
            )

            self.fields['Areas'].queryset = self.fields['Areas'].queryset.filter(
                localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
                localidade__unidade__empresasecundaria__status__in=['Mobilizado'],
                status__in=['Mobilizado'],
                localidade__status__in=['Mobilizado'],
                localidade__unidade__status__in=['Mobilizado']
            )

            all_choices = self.fields['TipoServico'].choices
            filtered_choices = [choice for choice in all_choices if choice[0] != 'Automático']
            self.fields['TipoServico'].choices = filtered_choices

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            self.fields['Areas'].queryset = self.fields['Areas'].queryset.filter(
                localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            )

            # Alterando o widget dos campos de seleção múltipla para SelectMultiple
            self.fields['ServicosEscalados'] = forms.ModelMultipleChoiceField(
                queryset=CatalogodeServicoLimpezaPredial.objects.filter(
                    EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                ),
                widget=forms.SelectMultiple(
                    attrs={
                        'class': 'form-control',  # Modifique a classe se necessário
                        'style': 'max-height: 40px; overflow-y: auto;'
                    }
                ),
                label='Serviços escalados',
                required=False,
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
        fields = ['Areas', 'TipoServico', 'DescricaoDoServico', 'TipoServico', 'ServicosEscalados', 'DataDeInicio',
                  'DataDeConclusao',]
        labels = {
            'Areas': 'Área',
            'TipoServico': 'Tipo de agendamento',
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
            'TipoServico': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'Areas': forms.Select(
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

class FatoServicoLimpezaPredialForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(FatoServicoLimpezaPredialForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type == 'creat/edit':
            self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                EmpresaSecundaria__status__in=['Mobilizado'],
                empresasecundaria__setor__setor__in=['Limpeza predial'],
                status__in=['Mobilizado']
            )

    class Meta:
        model = FatoServicoLimpezaPredial
        fields = ['Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Gerente', 'foto_entrega', ]

        labels = {
            'Servico': 'Serviço',
            'data_hora_chegada_na_area': 'Chegada na área',
            'data_hora_retorno_area': 'Retorno na área',
            'Gerente': 'Colaborador',
            'foto_entrega': 'Foto da área na entrega',
        }

        widgets = {
            'Servico': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'data_hora_chegada_na_area': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'DD/MM/AAAA HH:MM',
                }
            ),
            'data_hora_retorno_area': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'DD/MM/AAAA HH:MM',
                }
            ),
            'Gerente': forms.Select(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'DD/MM/AAAA HH:MM',
                }
            ),
            'foto_entrega': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }