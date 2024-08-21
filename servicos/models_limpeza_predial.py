from django.db import models
from utils.utils import generate_id_random
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from areas.models_limpeza_predial import AreaLimpezaPredial
from colaborador.models import Colaborador
from datetime import timedelta


class ServicoLimpezaPredialConfigurado(models.Model):
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
        related_name='Rarealimpezapredialconfigurado',
    )

    ServicosEscalados = models.ManyToManyField(
        to=CatalogodeServicoLimpezaPredial,
        blank=False,
        null=False,
        related_name='RServicosEscaladosLimpezaPredialServicoConfigurado'
    )

    diasaseremrealizado_options = [
        ('Segunda-Feira', 'Segunda-Feira'),
        ('Terça-Feira', 'Terça-Feira'),
        ('Quarta-Feira', 'Quarta-Feira'),
        ('Quinta-Feira', 'Quinta-Feira'),
        ('Sexta-Feira', 'Sexta-Feira'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    diasaseremrealizado = models.CharField(
        choices=diasaseremrealizado_options,
        null=False,
        blank=False,
        max_length=50,
        default=''
    )

    tempomedioplanejado = models.DurationField(
        null=False,
        blank=False,
        default=timedelta(minutes=30)
    )

    horario_1 = models.TimeField(
        null=False,
        blank=False,
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


class ServicoLimpezaPredialAgendado(models.Model):
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
        related_name='Rarealimpezapredialagendado',
    )

    ServicosEscalados = models.ManyToManyField(
        to=CatalogodeServicoLimpezaPredial,
        blank=False,
        null=False,
        related_name='RServicosEscaladosLimpezaPredialServicoAgendado'
    )

    # tempomedioplanejado = models.DurationField(
    #     null=False,
    #     blank=False,
    #     default=timedelta(minutes=30)
    # )

    DataDeInicio = models.DateTimeField(
        null=True,
        blank=True
    )

    DataDeConclusao = models.DateTimeField(
        blank=True,
        null=True
    )

    # horario_1 = models.TimeField(
    #     null=False,
    #     blank=False,
    # )
    #
    # horario_2 = models.TimeField(
    #     null=True,
    #     blank=True,
    # )
    #
    # horario_3 = models.TimeField(
    #     null=True,
    #     blank=True,
    # )
    #
    # horario_4 = models.TimeField(
    #     null=True,
    #     blank=True,
    # )
    #
    # horario_5 = models.TimeField(
    #     null=True,
    #     blank=True,
    # )
    #
    # horario_6 = models.TimeField(
    #     null=True,
    #     blank=True,
    # )
    #
    # horario_7 = models.TimeField(
    #     null=True,
    #     blank=True,
    # )
    #
    # horario_8 = models.TimeField(
    #     null=True,
    #     blank=True,
    # )
    #
    # horario_9 = models.TimeField(
    #     null=True,
    #     blank=True,
    # )

    def __str__(self):
        return f'{self.area} | {self.ServicosEscalados} | {self.DataDeInicio}'



class FatoServicoLimpezaPredial(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Servico = models.ForeignKey(
        to=ServicoLimpezaPredialAgendado,
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