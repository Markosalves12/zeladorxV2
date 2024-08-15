from django.db import models
from empresasecundario.models import EmpresaSecundaria

# Create your models here.
class CatalogoDeFerramentas(models.Model):
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
        related_name='REmpresaSecundariaCatalogoFerramentas',
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
        unique_together = ('nome', 'EmpresaSecundaria',)

    def __str__(self):
        return self.nome


class FerramentasDisponiveis(models.Model):
    Nome = models.ForeignKey(
        to=CatalogoDeFerramentas,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='RNomeCatalogoFerramentas'
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
        related_name='REmpresaSecundariaFerramentasDisponiveis',
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
        unique_together = ('Nome', 'EmpresaSecundaria')

    def __str__(self):
        return f'{self.Nome} -- {self.matricula}'