from unidade.models import Unidade
from django import forms
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.utils import define_empresas

class UnidadeForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(UnidadeForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if userid:
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']
            empresas_secundarias_ids = empresas['empresas_secundarias_ids']

            # Ajustar o queryset do campo 'empresaprimaria'
            self.fields['empresasecundaria'].queryset = self.fields['empresasecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids,
                id_random__in=empresas_secundarias_ids,
                status__in=['Mobilizado']
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
        fields = ['nome', 'linkmapajardinagem', 'linkmapalimnpezapredial', 'foto', 'empresasecundaria', ]
        labels = {
            'nome': 'Nome',
            'linkmapajardinagem': 'Link do mapa jardinagem da unidade',
            'linkmapalimnpezapredial': 'Link do mapa limpeza predial da unidade',
            'foto': 'Fotos da unidade',
            'EmpresaSecundaria': 'Empresa operadora',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'linkmapajardinagem': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'linkmapalimnpezapredial': forms.TextInput(
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