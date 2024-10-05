from unidade.models import Unidade
from django import forms
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.utils import define_empresas
from empresaprimaria.models import EmpresaPrimaria
from zeladorx.models import TypeZeladoria

class UnidadeForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(UnidadeForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']
        setores = empresas['setores']

        if userid:
            # Ajustar o queryset do campo 'empresaprimaria'
            self.fields['empresasecundaria'].queryset = self.fields['empresasecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids,
                id_random__in=empresas_secundarias_ids,
                status__in=['Mobilizado']
            )

        # habilitar_jardinagem = False
        # habilitar_limpeza = False
        #
        # # Checar os setores e definir se os campos devem ser habilitados
        # for objeto in TypeZeladoria.objects.filter(id__in=setores):
        #     if 'Jardinagem' in objeto.setor:
        #         habilitar_jardinagem = True
        #
        #     if 'Limpeza predial' in objeto.setor:
        #         habilitar_limpeza = True

        # Habilitar os campos se as condições forem verdadeiras
        if setores['habilitar_jardinagem']:
            self.fields['linkmapajardinagem'].widget = forms.TextInput(
                attrs={'class': 'form-control'}
            )
        else:
            self.fields.pop('linkmapajardinagem')

        if setores['habilitar_limpeza']:
            self.fields['linkmapalimnpezapredial'].widget = forms.TextInput(
                attrs={'class': 'form-control'}
            )
        else:
            self.fields.pop('linkmapalimnpezapredial')

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
        fields = ['nome', 'linkmapajardinagem', 'linkmapalimnpezapredial', 'foto', 'empresasecundaria']
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
            'foto': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }