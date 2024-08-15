from django import forms
from settings.models import SettingServicosGestor, SettingServicosGerente,SettingServicosColaborador



class SettingServicosGestorForms(forms.ModelForm):
    class Meta:
        model = SettingServicosGestor
        fields = ['Gestor','ServicoCompunsivo','TempoPadraoServico','NotificationToColaboborador',
                  'NotificationAceptReject','NotificationEndService', 'NotificationCancelService', 'NotificationNewService',]
        labels = {
            'Gestor': 'Nome',
            'ServicoCompunsivo': 'Definir todos os serviços como compulsivos?',
            'TempoPadraoServico': 'Definir um tempo padrão para todas os seus agendamentos?',
            'NotificationToColaboborador': 'Notificações obrigatórias para os colaboradores?',
            'NotificationAceptReject': 'Ser notificado se os colaboradores aceitam os rejeitam serviços?',
            'NotificationEndService': 'Ser notificado quando os serviços são finalizados?',
            'NotificationCancelService': 'Notificar seus colaboradores sobre o cancelamento de serviços?',
            'NotificationNewService': 'Notificar seus colaboradores sobre novos serviços?',
        }

        widgets = {
            'Gestor': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'ServicoCompunsivo': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'TempoPadraoServico': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationToColaboborador': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationAceptReject': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationEndService': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationCancelService': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationNewService': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class SettingServicosGerenteForms(forms.ModelForm):
    class Meta:
        model = SettingServicosGerente
        fields = ['Gerente','ServicoCompunsivo','TempoPadraoServico','NotificationToColaboborador',
                  'NotificationAceptReject','NotificationEndService', 'NotificationCancelService', 'NotificationNewService',]
        labels = {
            'Gerente': 'Nome',
            'ServicoCompunsivo': 'Definir todos os serviços como compulsivos?',
            'TempoPadraoServico': 'Definir um tempo padrão para todas os seus agendamentos?',
            'NotificationToColaboborador': 'Notificações obrigatórias para os colaboradores?',
            'NotificationAceptReject': 'Ser notificado se os colaboradores aceitam os rejeitam serviços?',
            'NotificationEndService': 'Ser notificado quando os serviços são finalizados?',
            'NotificationCancelService': 'Notificar seus colaboradores sobre o cancelamento de serviços?',
            'NotificationNewService': 'Notificar seus colaboradores sobre novos serviços?',
        }

        widgets = {
            'Gerente': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'ServicoCompunsivo': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'TempoPadraoServico': forms.TimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationToColaboborador': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationAceptReject': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationEndService': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationCancelService': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationNewService': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class SettingServicosColaboradorForms(forms.ModelForm):
    class Meta:
        model = SettingServicosColaborador
        fields = ['Colaborador','AceitarTodosOsServicos','RejeitarServicosPartirDe','RejeitarServicosAte',
                  'NotificationsNewService','NotificationsServiceCanceled', 'NotificationsAlterService']
        labels = {
            'Colaborador': 'Nome',
            'AceitarTodosOsServicos': 'Aceitar todos os servicos automaticamente?',
            'RejeitarServicosPartirDe': 'Rejeitar servicos a partir da data',
            'RejeitarServicosAte': 'Rejeitar servicos até a data',
            'NotificationsNewService': 'Ser notificado sobre novos servicos?',
            'NotificationsServiceCanceled': 'Ser notificado sobre servicos cancelados?',
            'NotificationsAlterService': 'Ser notificado sobre servicos alterados?',
        }

        widgets = {
            'Colaborador': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'AceitarTodosOsServicos': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'RejeitarServicosPartirDe': forms.DateTimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'RejeitarServicosAte': forms.DateTimeInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationsNewService': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationsServiceCanceled': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationsAlterService': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
        }