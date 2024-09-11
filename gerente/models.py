from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from utils.utils import generate_id_random
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from empresasecundario.models import EmpresaSecundaria
from notifications.utils import enviar_notificacao

# Create your models here.
class GerenteManager(BaseUserManager):
    def create_user(self, email, username, funcao, password=None, status='Mobilizado'):
        if not email:
            raise ValueError('O campo email deve ser preenchido')
        if not username:
            raise ValueError('O campo nome deve ser preenchido')
        if not funcao:
            raise ValueError('O campo função deve ser preenchido')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            funcao=funcao,
            status=status,
            id_random=generate_id_random()
        )

        if password:
            user.set_password(password)
        else:
            random_password = get_random_string(length=20)

            enviar_notificacao(
                destinatario=[self.email],
                assunto="Novo gerente",
                contexto={
                    'username': self.username,
                    'email': self.email,
                    'cargo': 'gerente',
                    'empresa': self.EmpresaSecundaria,
                    'senha': random_password
                },
                template='notifications/adicao_gestor.html'
            )

            self.password = make_password(random_password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, funcao, password):
        user = self.create_user(
            email=email,
            username=username,
            funcao=funcao,
            password=password,
            # gestor=gestor,
            status='Mobilizado'
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Gerente(AbstractBaseUser, PermissionsMixin):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    username = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    email = models.EmailField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )

    funcao = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    password = models.CharField(
        max_length=128,  # Alterado para suportar hashes de senha
        blank=True,
        null=True
    )

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

    is_active = models.BooleanField(
        default=True
    )

    is_admin = models.BooleanField(
        default=False
    )

    empresasecundaria = models.ManyToManyField(
        to=EmpresaSecundaria,
        # on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='REmpresaSecundariagerente'
    )

    groups = models.ManyToManyField(
        Group,
        related_name='gerente_set',  # Renomeia o acessor reverso
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='gerente_permissions_set',  # Renomeia o acessor reverso
        blank=True,
    )

    objects = GerenteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'funcao', 'username']

    def __str__(self):
        return self.username


    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()

        if self.username:
            self.username = self.username.strip().capitalize()

        if self.funcao:
            self.funcao = self.funcao.strip().capitalize()

        super(Gerente, self).save(*args, **kwargs)

    # função dispara a senha por email caso o campo senha esteja em braco
    # nesse caso isso é ativado nos formularios html
    # pelo admin do django pode se criar alterar manualemnte

    def save(self, *args, **kwargs):
        if not self.pk and not self.password:
            random_password = get_random_string(
                length=12
            )
            enviar_notificacao(
                destinatario=[self.email],
                assunto="Novo gerente",
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
        return self.is_active