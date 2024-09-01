from servicos.models_jardinagem import ServicoJardinagemAgendado, FatoServicoJardinagem
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from colaborador.models import Colaborador
from django import forms

class ServicoJaridinagemAgendadoForms(forms.ModelForm):
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
        queryset=Colaborador.objects.all(),
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
                  'DescricaoDoServico', 'Areas', 'foto_solicitacao', 'foto_entrega', 'ServicoCompunsivo']

        labels = {
            'DataDeInicio': 'Data marcada para inicio',
            'DataDeConclusao': 'Data prevista para conclusao',
            'ServicosEscalados': 'Serviços Escalados',
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
    def __init__(self, *args, id_random_servico=None, empresa=None, **kwargs):
        super(FatoServicoJardinagemForms, self).__init__(*args, **kwargs)
        if id_random_servico is not None:
            self.fields['Servico'].queryset = self.fields['Servico'].queryset.exclude(
                status__in=['Cancelado', 'Concluido']
            ).filter(
                id_random=id_random_servico
            )

    class Meta:
        model = FatoServicoJardinagem
        fields = ['Servico', 'data_hora_chegada_na_area', 'EquipamentoUsado', 'data_hora_retorno_area', 'Colaborador']

        labels = {
            'Servico': 'Serviço agendado',
            'data_hora_chegada_na_area': 'Chegada na área',
            'EquipamentoUsado': 'Equipamento usado',
            'data_hora_retorno_area': 'Retorno da área',
            'Colaborador': 'Colaborador',
        }

        widgets = {
            'Servico': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'data_hora_chegada_na_area': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'class': 'form-control'
                }
            ),
            'EquipamentoUsado': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'data_hora_retorno_area': forms.DateInput(
                format='%d/%m/%Y',
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
