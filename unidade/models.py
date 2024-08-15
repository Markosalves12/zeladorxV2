from django.db import models
from empresasecundario.models import EmpresaSecundaria
from utils.utils import generate_id_random

# Create your models here.
class Unidade(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    nome = models.CharField(
        blank=False,
        null=False,
        max_length=100,
        unique=True
    )

    linkmapa = models.CharField(
        blank=True,
        null=True,
        max_length=300
    )

    foto = models.ImageField(
        upload_to="media/%Y/%m/%d/",
        blank=True,
    )

    EmpresaSecundaria = models.ForeignKey(
        to=EmpresaSecundaria,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='REmpresaSecundariaUnidade'
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
        return self.nome