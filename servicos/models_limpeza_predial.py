from django.db import models
from utils.utils import generate_id_random
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from areas.models_limpeza_predial import AreaLimpezaPredial
from colaborador.models import Colaborador

class ServicoLimpezaPredial(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    area = models.ForeignKey(
        to=AreaLimpezaPredial,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='Rarealimpezapredial',
    )

    ServicosEscalados = models.ManyToManyField(
        to=CatalogodeServicoLimpezaPredial,
        blank=False,
        null=False,
        related_name='RServicosEscaladosLimpezaPredialServicoAgendado'
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

    horario_6 = models.TimeField(
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

    horario_9 = models.TimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.area} | {self.ServicosEscalados}'



class FatoServicoLimpezaPredial(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Servico = models.ForeignKey(
        to=ServicoLimpezaPredial,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="RServicoServicoLimpezaPredialAgendado"
    )

    data_hora_chegada_na_area = models.DateTimeField(
        blank=False,
        null=False
    )

    data_hora_retorno_area = models.DateTimeField(
        blank=False,
        null=False
    )

    Colaborador = models.ForeignKey(
        to=Colaborador,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='RColaboradorFatoServicoLimpezaPredial'
    )