from django import forms
from areas.models_limpeza_predial import AreaLimpezaPredial
from empresasecundario.utils import define_empresa_primaria_ids

class AreasLimpezaPredialForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(AreasLimpezaPredialForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if userid:
            # Ajustar o queryset do campo 'empresaprimaria'
            empresas_primarias_ids = define_empresa_primaria_ids(request=request, userid=userid)
            self.fields['localidade'].queryset = self.fields['localidade'].queryset.filter(
                unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids
            )

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



