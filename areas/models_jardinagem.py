from django.db import models
from vegetacao.models import CatalogoVegetacao
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from localidade.models_Jardinagem import LocalidadeJardiangem
from terrenos.models import Terreno
from utils.utils import generate_id_random


# Create your models here.
class AreasJardins(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    nome = models.CharField(
        blank=False,
        null=False,
        max_length=100,
    )

    dimensao = models.FloatField(
        blank=True,
        null=True
    )

    Terreno = models.ForeignKey(
        to=Terreno,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='rTerrenoAreas'
    )

    vegetacao = models.ForeignKey(
        to=CatalogoVegetacao,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='vegetacaocatalogovegetacao'
    )

    servico = models.ForeignKey(
        to=CatalogodeServicoJardinagem,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='servicocatalogoservico'
    )

    localidade = models.ForeignKey(
        to=LocalidadeJardiangem,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='localidadeareas'
    )

    foto = models.ImageField(
        upload_to="media/%Y/%m/%d/",
        blank=True,
    )

    periodicidade_options = [
        ('Mensal', 'Mensal'),
        ('Semanal', 'Semanal'),
        ('Quinzenal', 'Quinzenal'),
        ('Bimestral', 'Bimestral'),
        ('Trimestral', 'Trimestral'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
    ]

    periodicidade = models.CharField(
        blank=False,
        null=False,
        choices=periodicidade_options,
        default='Mensal',
        max_length=30
    )

    status_options = [
        ('Mobilizado', 'Mobilizado'),
        ('Desmobilizado', 'Desmobilizado'),
        ('Desmobilizaçao permanente', 'Desmobilizaçao permanente'),
        ('Deletado', 'Deletado'),
    ]

    status = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=status_options,
        default='Mobilizado'
    )

    class Meta:
        unique_together = ('nome', 'vegetacao', 'Terreno')

    def __str__(self):
        return self.nome