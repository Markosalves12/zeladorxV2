from django.db import models
from utils.utils import generate_id_random
from gerente.models import Gerente

# Create your models here.
class ForumJardinagem(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    nome = models.CharField(
        max_length=255
    )

    descricao = models.TextField(
        blank=True,
        null=True
    )

    criador = models.ForeignKey(
        to=Gerente,  # Ou outro usuário que pode criar fóruns
        on_delete=models.CASCADE,
        related_name='foruns_criados'
    )

    participantes = models.ManyToManyField(
        to=Gerente,
        related_name='foruns_participantes',
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-criado_em']  # Sempre listar os mais recentes primeiro

    def __str__(self):
        return self.nome


class MensagemJardinagem(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    TEXTO = 'texto'
    IMAGEM = 'imagem'
    ARQUIVO = 'arquivo'

    TIPOS_MENSAGEM = [
        (TEXTO, 'Texto'),
        (IMAGEM, 'Imagem'),
        (ARQUIVO, 'Arquivo'),
    ]

    forum = models.ForeignKey(
        to=ForumJardinagem,
        on_delete=models.CASCADE,
        related_name="mensagens"
    )

    remetente = models.ForeignKey(
        to=Gerente,
        on_delete=models.CASCADE
    )

    conteudo = models.TextField()  # Permite mensagens mais longas

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS_MENSAGEM,
        default=TEXTO
    )

    arquivo = models.FileField(
        upload_to="chats/arquivos/",
        blank=True,
        null=True
    )  # Para imagens ou arquivos

    enviado_em = models.DateTimeField(
        auto_now_add=True
    )

    editado_em = models.DateTimeField(
        auto_now=True
    )  # Atualiza sempre que a mensagem for editada

    class Meta:
        ordering = ['-enviado_em']  # Mais recentes primeiro

    def __str__(self):
        return f"{self.remetente} -> {self.forum}"
