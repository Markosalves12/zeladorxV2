from django.db import models
from utils.utils import generate_id_random
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial

class ServicoLimpezaPredial:
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    ServicosEscalados = models.ManyToManyField(
        to=CatalogodeServicoLimpezaPredial,
        blank=False,
        null=False,
        related_name='RServicosEscaladosLimpezaPredialServicoAgendado'
    )

    # data_prestacao =

    horario_1 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_1 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_2 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_3 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_4 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_5 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_7 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_8 = models.TimeField(
        null=True,
        blank=True,
    )



