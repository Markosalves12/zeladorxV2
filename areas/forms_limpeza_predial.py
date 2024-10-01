from django import forms
from areas.models_limpeza_predial import AreaLimpezaPredial
from empresasecundario.utils import define_empresas

class AreasLimpezaPredialForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type='creat/edit', **kwargs):
        super(AreasLimpezaPredialForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if userid:
            # Ajustar o queryset do campo 'empresaprimaria'
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']
            empresas_secundarias_ids = empresas['empresas_secundarias_ids']

            self.fields['localidade'].queryset = self.fields['localidade'].queryset.filter(
                unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
                unidade__empresasecundaria__status__in=['Mobilizado'],
                status__in=['Mobilizado'],
                unidade__status__in=['Mobilizado'],
            )

            self.fields['servico'].queryset = self.fields['servico'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                EmpresaSecundaria__status__in=['Mobilizado'],
                status__in=['Mobilizado']
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

    class Meta:
        model = AreaLimpezaPredial
        fields = ['nome', 'dimensao', 'servico', 'localidade', 'foto']

        labels = {
            'nome': 'Nome da região',
            'dimensao': 'Dimensão da área em M²',
            'servico': 'Serviço principal aplicado',
            'localidade': 'Localidade',
            'foto': 'Foto da região',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'dimensao': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'servico': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'localidade': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'foto': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }



