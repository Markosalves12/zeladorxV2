from django.db import models
from empresasecundario.models import EmpresaSecundaria
from utils.utils import generate_id_random

# Create your models here.
class EquipamentoDisponiveisJardinagem(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Nome = models.CharField(
        max_length=60,
        blank=False,
        null=False,
    )

    DataDeAquisicao = models.DateField(
        blank=False,
        null=False,
    )

    DataDeDesmobilizacao = models.DateField(
        blank=True,
        null=True,
    )
    
    matricula = models.CharField(
        blank=False,
        null=False,
        max_length=12,
    )

    EmpresaSecundaria = models.ForeignKey(
        to=EmpresaSecundaria,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='REmpresaSecundariaEquipamentosDisponiveisJardinagem',
    )


    tipoequipamento_options = [
        ('Proprio', 'Proprio'),
        ('Terceirizado', 'Terceirizado')
    ]

    tipoequipamento = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=tipoequipamento_options,
        default='Proprio'
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

    def __str__(self):
        return f'{self.Nome} -- {self.matricula}'