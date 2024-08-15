from django.db import models
from utils.utils import generate_id_random
from gestor.models import Gestor
from gerente.models import Gerente
from colaborador.models import Colaborador

# Create your models here.
class SettingServicosGestor(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Gestor = models.ForeignKey(
        to=Gestor,
        null=False,
        blank=False,
        related_name='RGestorSettingServicosGestor',
        on_delete=models.CASCADE,
    )

    ServicoCompunsivo = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    TempoPadraoServico = models.DurationField(
        blank=True,
        null=True,
    )

    NotificationToColaboborador = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationAceptReject = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationEndService = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationCancelService = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationNewService = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

class SettingServicosGerente(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Gerente = models.ForeignKey(
        to=Gerente,
        null=False,
        blank=False,
        related_name='RGerenteSettingServicosGerente',
        on_delete=models.CASCADE,
    )

    ServicoCompunsivo = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    TempoPadraoServico = models.DurationField(
        blank=True,
        null=True,
    )

    NotificationToColaboborador = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationAceptReject = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationEndService = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationCancelService = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationNewService = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

class SettingServicosColaborador(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Colaborador = models.ForeignKey(
        to=Colaborador,
        null=False,
        blank=False,
        related_name='RColaboradorSettingServicosColaborador',
        on_delete=models.CASCADE,
    )

    AceitarTodosOsServicos = models.BooleanField(
        blank=True,
        null=True,
        default=True
    )

    RejeitarServicosPartirDe = models.DateTimeField(
        blank=True,
        null=True,
    )

    RejeitarServicosAte = models.DateTimeField(
        blank=True,
        null=True,
    )

    NotificationsNewService = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationsServiceCanceled = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationsAlterService = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )