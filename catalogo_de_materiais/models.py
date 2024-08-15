from django.db import models
from empresasecundario.models import EmpresaSecundaria
from utils.utils import generate_id_random

# Create your models here.
class ConsumoMateriais(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    nome = models.CharField(
        blank=False,
        null=False,
        max_length=30,
    )

    EmpresaSecundaria = models.ForeignKey(
        to=EmpresaSecundaria,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='REmpresaSecundariaConsumo'
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
        unique_together = ('nome', 'EmpresaSecundaria', )

    def __str__(self):
        return f'{self.nome}'


class CategoriaMaterial(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    nome = models.CharField(
        blank=False,
        null=False,
        max_length=30,
    )

    EmpresaSecundaria = models.ForeignKey(
        to=EmpresaSecundaria,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='REmpresaSecundariaCategoriaMateriais',
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
        unique_together = ('nome', 'EmpresaSecundaria', )

    def __str__(self):
        return f'{self.nome}'



class CatalogoMaterial(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    nome = models.CharField(
        blank=False,
        null=False,
        max_length=30,
    )

    EmpresaSecundaria = models.ForeignKey(
        to=EmpresaSecundaria,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='REmpresaSecundariaCatalogoMaterial'
    )

    CategoriaDoMaterial = models.ForeignKey(
        to=CategoriaMaterial,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='RCategoriaDoMaterial'
    )

    FormaDeConsumo = models.ForeignKey(
        to=ConsumoMateriais,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='RFormaDeConsumo'
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
        unique_together = (
            'nome',
            'EmpresaSecundaria',
            'CategoriaDoMaterial',
            'FormaDeConsumo',
        )

    def __str__(self):
        return f'{self.nome} -- {self.FormaDeConsumo}'