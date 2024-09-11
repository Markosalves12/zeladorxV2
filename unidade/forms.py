from unidade.models import Unidade
from django import forms
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.utils import define_empresa_primaria_ids

class UnidadeForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(UnidadeForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if userid:
            empresas_primarias_ids = define_empresa_primaria_ids(request=request, userid=userid)

            # Ajustar o queryset do campo 'empresaprimaria'
            self.fields['empresasecundaria'].queryset = self.fields['empresasecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids
            )

    empresasecundaria = forms.ModelMultipleChoiceField(
        queryset=EmpresaSecundaria.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Empresas que atende',
        required=True  # Defina como True se a seleção de colaboradores for obrigató
    )

    class Meta:
        model = Unidade
        fields = ['nome', 'linkmapa', 'foto', 'empresasecundaria', ]
        labels = {
            'nome': 'Nome',
            'linkmapa': 'Link do mapa da unidade',
            'foto': 'Fotos da unidade',
            'EmpresaSecundaria': 'Empresa operadora',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'linkmapa': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'foto': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            # 'empresasecundaria': forms.Select(
            #     attrs={
            #         'class': 'form-control'
            #     }
            # )
        }