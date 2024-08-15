from django.db import models
from utils.utils import generate_id_random
from utils.utils import resize_image

# Create your models here.
class EmpresaPrimaria(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    nome = models.CharField(
        blank=False,
        null=False,
        max_length=120,
    )

    razao_social = models.CharField(
        blank=False,
        null=False,
        max_length=120,
    )

    CNPJ = models.CharField(
        blank=False,
        null=False,
        max_length=40,
        unique=True
    )

    username = models.CharField(
        blank=False,
        null=False,
        max_length=40
    )

    password = models.CharField(
        blank=False,
        null=False,
        max_length=120
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

    logo = models.ImageField(
        upload_to="media/%Y/%m/%d/",
        blank=True,
        null=True,
        max_length=1000
    )

    def save(self, *args, **kwargs):
        if self.logo:
            self.logo = resize_image(self.logo, 40)

        super(EmpresaPrimaria, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome

