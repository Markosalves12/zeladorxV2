from django.db import models
from utils.utils import generate_id_random
from gerente.models import Gerente

# Create your models here.
class PermissionsJardinagem(models.Model):
    # conluna principal usada como parametro de urls
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    permissions_CRUD = [
        ('250: Pode criar novas áreas de jardinagem', '250: Pode criar novas áreas de jardinagem'),
        ('251: Pode editar áreas de jardinagem', '251: Pode editar áreas de jardinagem'),
        ('252: Pode visualizar áreas de jardinagem', '252: Pode visualizar áreas de jardinagem'),
        ('253: Pode excluir áreas de jardinagem', '253: Pode excluir áreas de jardinagem'),

        ('254: Pode criar novas localidades', '254: Pode criar novas localidades'),
        ('255: Pode editar localidades', '255: Pode editar localidades'),
        ('256: Pode visualizar localidades', '256: Pode visualizar localidades'),
        ('257: Pode excluir localidades', '257: Pode excluir localidades'),

        ('258: Pode criar novos terrenos', '258: Pode criar novos terrenos'),
        ('259: Pode editar terrenos', '259: Pode editar terrenos'),
        ('260: Pode visualizar terrenos', '260: Pode visualizar terrenos'),
        ('261: Pode excluir terrenos', '261: Pode excluir terrenos'),

        ('262: Pode criar novas vegetações', '262: Pode criar novas vegetações'),
        ('263: Pode editar vegetações', '263: Pode editar vegetações'),
        ('264: Pode visualizar vegetações', '264: Pode visualizar vegetações'),
        ('265: Pode excluir vegetações', '265: Pode excluir vegetações'),

        ('266: Pode criar novos serviços ao catálogo', '266: Pode criar novos serviços ao catálogo'),
        ('267: Pode editar serviços do catálogo', '267: Pode editar serviços do catálogo'),
        ('268: Pode visualizar serviços do catálogo', '268: Pode visualizar serviços do catálogo'),
        ('269: Pode excluir serviços do catálogo', '269: Pode excluir serviços do catálogo'),

        ('270: Pode criar novos colaboradores', '270: Pode criar novos colaboradores'),
        ('271: Pode editar colaboradores', '271: Pode editar colaboradores'),
        ('272: Pode visualizar colaboradores', '272: Pode visualizar colaboradores'),
        ('273: Pode excluir colaboradores', '273: Pode excluir colaboradores'),

        ('274: Pode criar novos gerentes', '274: Pode criar novos gerentes'),
        ('275: Pode editar gerentes', '275: Pode editar gerentes'),
        ('276: Pode visualizar gerentes', '276: Pode visualizar gerentes'),
        ('277: Pode excluir gerentes', '277: Pode excluir gerentes'),

        ('278: Pode agendar novos serviços', '278: Pode agendar novos serviços'),
        ('279: Pode editar serviços agendados', '279: Pode editar serviços agendados'),
        ('280: Pode visualizar serviços agendados', '280: Pode visualizar serviços agendados'),
        ('281: Pode excluir serviços agendados', '281: Pode excluir serviços agendados'),

        ('282: Pode acompanhar serviços agendados', '282: Pode acompanhar serviços agendados'),
        ('283: Pode editar serviços em andamento', '283: Pode editar serviços em andamento'),
        ('284: Pode concluir serviços em andamento', '284: Pode concluir serviços em andamento'),

        ('285: Pode extrair relatórios XLSX', '285: Pode extrair relatórios XLSX'),
        ('286: Pode extrair relatórios PDF', '286: Pode extrair relatórios PDF'),

        ('287: Pode editar permissões dos gerentes', '287: Pode editar permissões dos gerentes'),
        ('288: Pode editar permissões dos colaboradores', '288: Pode editar permissões dos colaboradores'),
        ('289: Pode visualizar permissões dos colaboradores', '289: Pode visualizar permissões dos colaboradores'),
    ]

    Permissions = models.CharField(
        choices=permissions_CRUD,
        null=False,
        blank=False,
        unique=True,
        max_length=75
    )

    def __str__(self):
        return self.Permissions


class PermissionsAccessJardinagem(models.Model):
    # conluna principal usada como parametro de urls
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Gerente = models.ForeignKey(
        to=Gerente,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    Permissions = models.ManyToManyField(
        to=PermissionsJardinagem,
        null=False,
        blank=False,
        related_name='RPermissionsAccess'
    )