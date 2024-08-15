from django.db import models
from equipamentos.models import EquipamentoDisponiveis
from empresasecundario.models import EmpresaSecundaria
from utils.utils import generate_id_random

# Create your models here.
class CatalogoManutencao(models.Model):
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
        related_name='REmpresaSecundariaTipoManutencao'
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
        )

    def __str__(self):
        return f'{self.nome}'

class MotivoDaManutencao(models.Model):
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

    EmpresaSecundaria = models.ForeignKey(
        to=EmpresaSecundaria,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='REmpresaSecundariaMotivoManutencao'
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


class ManutencaoDeEquipamentos(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Equipamento = models.ForeignKey(
        to=EquipamentoDisponiveis,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='REquipamentoDisponivel'
    )

    DataDeInicio = models.DateTimeField(
        null=False,
        blank=False,
    )

    DataFim = models.DateTimeField(
        null=False,
        blank=False,
    )

    CatalogoManutencao = models.ForeignKey(
        to=CatalogoManutencao,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='RCatalogoManutencao'
    )

    MotivoManutencao = models.ForeignKey(
        to=MotivoDaManutencao,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='RMotivoManutencao'
    )

    Descricaodoservico = models.TextField(
        blank=True,
        null=True,
        max_length=500
    )