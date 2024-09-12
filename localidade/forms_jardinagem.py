from django import forms
from localidade.models_Jardinagem import LocalidadeJardiangem
from empresasecundario.utils import define_empresa_primaria_ids


class LocalidadeJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(LocalidadeJardinagemForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if userid:
            # Ajustar o queryset do campo 'empresaprimaria'
            empresas_primarias_ids = define_empresa_primaria_ids(request=request, userid=userid)
            self.fields['unidade'].queryset = self.fields['unidade'].queryset.filter(
                empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids
            )

    class Meta:
        model = LocalidadeJardiangem
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