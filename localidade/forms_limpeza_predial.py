from django import forms
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from empresasecundario.utils import define_empresas

class LocalidadeLimpezaPredialForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(LocalidadeLimpezaPredialForms, self).__init__(*args, **kwargs)
        if userid:
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']
            empresas_secundarias_ids = empresas['empresas_secundarias_ids']

            self.fields['unidade'].queryset = self.fields['unidade'].queryset.filter(
                empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                empresasecundaria__id_random__in=empresas_secundarias_ids,
                status__in=['Mobilizado']
            )

    class Meta:
        model = LocalidadeLimpezaPredial
        fields = ['nome', 'lat_med', 'long_med', 'unidade', ]
        labels = {
            'nome': 'Localidade',
            'lat_med': 'Latitude média',
            'long_med': 'Longitude média',
            'unidade': 'Unidade'
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'lat_med': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'long_med': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'unidade': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }