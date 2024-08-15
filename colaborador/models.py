from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from utils.utils import generate_id_random
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db import models
from gerente.models import Gerente
from notifications.utils import enviar_notificacao

# Create your models here.
class ColaboradorManager(BaseUserManager):
    def create_user(self, email, username, funcao, password=None, gerente=None, status='Mobilizado'):
        if not email:
            raise ValueError('O campo email deve ser preenchido')
        if not username:
            raise ValueError('O campo username deve ser preenchido')
        if not funcao:
            raise ValueError('O campo função deve ser preenchido')
        if not gerente:
            raise ValueError('O campo gerente deve ser preenchido')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            funcao=funcao,
            gerente=gerente,
            status=status,
            id_random=generate_id_random()
        )

        if password:
            user.set_password(password)
        else:
            random_password = get_random_string(length=12)

            enviar_notificacao(
                destinatario=[self.email],
                assunto="Novo colaborador",
                contexto={
                    'username': self.username,
                    'email': self.email,
                    'cargo': 'gerente',
                    'empresa': '',
                    'senha': random_password
                },
                template='notifications/adicao_gestor.html'
            )

            self.password = make_password(random_password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, funcao, password, gerente):
        user = self.create_user(
            email=email,
            username=username,
            funcao=funcao,
            password=password,
            gerente=gerente,
            status='Mobilizado'
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# modelo de colaborador
class Colaborador(AbstractBaseUser, PermissionsMixin):
    # conluna principal usada como parametro de urls
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    # coluna que recebe o nome do colaborado
    username = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=False
    )
    # email de contato do colaborador
    # opcional no contexto no projeto
    email = models.EmailField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
    )

    # função que o colaboradorn exerce no contexto
    funcao = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    # atividades exercidas pelos colaboradores
    atividades = models.TextField(
        blank=False,
        null=False,
        max_length=150
    )

    password = models.CharField(
        max_length=128,  # Alterado para suportar hashes de senha
        blank=True,
        null=True
    )

    # gerente imediato do colaborador
    gerente = models.ManyToManyField(
        to=Gerente,
        blank=False,
        null=False,
        related_name='Rgerentegerenteorigem'
    )

    # a coluna status controla a disponibilidade do objeto no formularios espalhados pelo sistema
    status_options = [
        ('Mobilizado', 'Mobilizado'),
        ('Desmobilizado', 'Desmobilizado'),
        ('Desmobilizacao Permanente', 'Desmobilizacao Permanente')
    ]
    status = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=status_options,
        default='Mobilizado'
    )

    # os colaboradores criados não tem acesso a rota admin do django
    # com privilégio de super usário
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    # controle de permissões padrões dos colaboradores
    # permissão zeradas temporarioamente
    groups = models.ManyToManyField(
        Group,
        related_name='colaborador_set',  # Renomeia o acessor reverso
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='colaborador_permissions_set',  # Renomeia o acessor reverso
        blank=True,
    )

    # colaboiradores são objetos gerenciados por
    # ColaboradorManager
    objects = ColaboradorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'funcao', 'gerente']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()

        if self.username:
            self.username = self.username.strip().capitalize()

        if self.funcao:
            self.funcao = self.funcao.strip().capitalize()

        super(Colaborador, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk and not self.password:  # only if the object is being created and senha is not provided
            random_password = get_random_string(length=12)

            enviar_notificacao(
                destinatario=[self.email],
                assunto="Novo colaborador",
                contexto={
                    'username': self.username,
                    'email': self.email,
                    'cargo': 'gerente',
                    'empresa': '',
                    'senha': random_password
                },
                template='notifications/adicao_gestor.html'
            )

            self.password = make_password(random_password)

        else:
            self.password = make_password(self.password)


        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_staff(self):
        return self.is_admin
