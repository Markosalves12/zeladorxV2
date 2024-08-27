from django.db import models

# Create your models here.
class DiasDaSemana(models.Model):
    diasdasemana = models.CharField(
        max_length=60,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.diasdasemana