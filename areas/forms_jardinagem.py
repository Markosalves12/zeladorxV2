from django import forms
from areas.models_jardinagem import AreasJardins
from empresasecundario.utils import define_empresas


class AreasJardinsForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type='creat/edit', **kwargs):
        super(AreasJardinsForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        # Ajustar o queryset do campo 'empresaprimaria'
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type=='creat/edit':
            self.fields['localidade'].queryset = self.fields['localidade'].queryset.filter(
                unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
                unidade__empresasecundaria__status__in=['Mobilizado'],
                status__in=['Mobilizado'],
                unidade__status__in=['Mobilizado'],
            ).distinct()

            self.fields['servico'].queryset = self.fields['servico'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                EmpresaSecundaria__status__in=['Mobilizado'],
                status__in=['Mobilizado']
            ).distinct()

            self.fields['vegetacao'].queryset = self.fields['vegetacao'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                EmpresaSecundaria__status__in=['Mobilizado'],
                status__in=['Mobilizado']
            ).distinct()

            self.fields['Terreno'].queryset = self.fields['Terreno'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                EmpresaSecundaria__status__in=['Mobilizado'],
                status__in=['Mobilizado']
            ).distinct()

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            self.fields['localidade'].queryset = self.fields['localidade'].queryset.filter(
                unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            ).distinct()

            self.fields['servico'].queryset = self.fields['servico'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            ).distinct()

            self.fields['vegetacao'].queryset = self.fields['vegetacao'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            ).distinct()

            self.fields['Terreno'].queryset = self.fields['Terreno'].queryset.filter(
                EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            ).distinct()

    class Meta:
        model = AreasJardins
        fields = ['nome', 'dimensao', 'Terreno', 'vegetacao', 'servico', 'localidade', 'foto', 'periodicidade']

        labels = {
            'nome': 'Nome da região',
            'dimensao': 'Dimensão da área em M²',
            'vegetacao': 'Vegetação predominante',
            'Terreno': 'Terreno predominante',
            'servico': 'Serviço principal aplicado',
            'localidade': 'Localidade',
            'foto': 'Foto da região',
            'periodicidade': 'Periodicidade de retorno'
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
            'Terreno': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'vegetacao': forms.Select(
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
            'periodicidade': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
