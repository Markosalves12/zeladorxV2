from servicos.models_jardinagem import ServicoJardinagemAgendado, FatoServicoJardinagem
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from gerente.models import Gerente
from django import forms
from empresasecundario.utils import define_empresas

class ServicoJaridinagemAgendadoForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(ServicoJaridinagemAgendadoForms, self).__init__(*args, **kwargs)
        if userid:
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']
            empresas_secundarias_ids = empresas['empresas_secundarias_ids']

            self.fields['ServicosEscalados'].queryset = self.fields['ServicosEscalados'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                EmpresaSecundaria__status__in=['Mobilizado'],
                status__in=['Mobilizado']
            )

            self.fields['ColaboradoresEscalados'].queryset = self.fields['ColaboradoresEscalados'].queryset.filter(
                empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                empresasecundaria__id_random__in=empresas_secundarias_ids,
                empresasecundaria__status__in=['Mobilizado'],
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

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            self.fields['ServicosEscalados'].widget = forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )

            self.fields['ColaboradoresEscalados'].widget = forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )

        choices_filtrados = [option for option in self.fields['TipoServico'].choices if option[0] != 'Automático']
        # Definindo as novas opções filtradas
        self.fields['TipoServico'].choices = choices_filtrados

    ServicosEscalados = forms.ModelMultipleChoiceField(
        queryset=CatalogodeServicoJardinagem.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Serviços escalados',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    ColaboradoresEscalados = forms.ModelMultipleChoiceField(
        queryset=Gerente.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Colaboradores escalado',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    class Meta:
        model = ServicoJardinagemAgendado
        fields = ['DataDeInicio', 'DataDeConclusao', 'ServicosEscalados', 'ColaboradoresEscalados',
                  'DescricaoDoServico', 'Areas', 'TipoServico', 'foto_solicitacao', 'foto_entrega', 'ServicoCompunsivo']

        labels = {
            'DataDeInicio': 'Data marcada para inicio',
            'DataDeConclusao': 'Data prevista para conclusao',
            'ServicosEscalados': 'Serviços Escalados',
            'TipoServico': 'Tipo de agendamento',
            'ColaboradoresEscalados': 'Colaboradores escalados',
            'DescricaoDoServico': 'Descrição do serviço',
            'Areas': 'Area para ser atendida',
            'foto_solicitacao': 'Foto da área na solicitação',
            'foto_entrega': 'Foto da área na entrega',
            'ServicoCompunsivo': 'Serviço compulsivo'
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
            'foto_solicitacao': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'foto_entrega': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'ServicoCompunsivo': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class FatoServicoJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, id_random=str, **kwargs):
        super(FatoServicoJardinagemForms, self).__init__(*args, **kwargs)
        self.fields['Servico'].queryset = self.fields['Servico'].queryset.filter(
            id_random=id_random
        )

        self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
            status__in=['Mobilizado']
        )

    class Meta:
        model = FatoServicoJardinagem
        fields = ['Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Gerente']

        labels = {
            'Servico': 'Serviço agendado',
            'data_hora_chegada_na_area': 'Chegada na área',
            'data_hora_retorno_area': 'Retorno da área',
            'Colaborador': 'Colaborador',
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
                    'class': 'form-control'
                }
            ),
        }
