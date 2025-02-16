from django import forms
from chats.models import ForumJardinagem, MensagemJardinagem
from empresasecundario.utils import define_empresas
from gerente.models import Gerente

class ForumJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type='creat/edit', id_random=False, **kwargs):
        super(ForumJardinagemForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        # Ajustar o queryset do campo 'empresaprimaria'
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type=='creat/edit':
            self.fields['criador'].queryset = self.fields['criador'].queryset.filter(
                id_random=userid
            )

            self.fields['participantes'].queryset = self.fields['participantes'].queryset.filter(
                empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                empresasecundaria__id_random__in=empresas_secundarias_ids,
            ).distinct()

    participantes = forms.ModelMultipleChoiceField(
        queryset=Gerente.objects.distinct(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Participantes',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    class Meta:
        model = ForumJardinagem
        fields = ['nome', 'descricao', 'criador', 'participantes']

        labels = {
            'nome': 'Nome',
            'descricao': 'Descricao',
            'criador': 'Criador',
            'participantes': 'Participantes',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'descricao': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'criador': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class MensagemJardinagemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['arquivo'].required = False  # Permite enviar mensagens sem arquivos

    class Meta:
        model = MensagemJardinagem
        fields = ['conteudo', 'arquivo']

        labels = {
            'conteudo': '',
            'arquivo': '',
        }

        widgets = {
            'conteudo': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 1,  # Altura inicial de uma linha
                    'style': 'max-height: 150px; min-height: 40px; overflow-y: auto; resize: none;'
                }
            ),
            'arquivo': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'style': 'height: 40px;'
                }
            ),
        }