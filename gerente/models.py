from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string
from empresasecundario.models import EmpresaSecundaria
from notifications.utils import enviar_notificacao
from utils.utils import generate_id_random


class GerenteManager(BaseUserManager):
    def create_user(self, email, username, password=None, status='Mobilizado'):
        if not email:
            raise ValueError('O campo email deve ser preenchido')
        if not username:
            raise ValueError('O campo nome deve ser preenchido')

        email = self.normalize_email(email.strip().lower())
        username = username.strip().capitalize()

        # Gera senha aleatória se não for fornecida
        if not password:
            password = get_random_string(length=12)
            enviar_notificacao(
                destinatario=[email],
                assunto="Novo gerente",
                contexto={
                    'username': username,
                    'email': email,
                    'cargo': 'gerente',
                    'empresa': '',
                    'senha': password
                },
                template='notifications/adicao_gestor.html'
            )

        user = self.model(
            email=email,
            username=username,
            status=status
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password, status='Mobilizado')
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Gerente(AbstractBaseUser):
    STATUS_OPCOES = [
        ('Mobilizado', 'Mobilizado'),
        ('Desmobilizado', 'Desmobilizado'),
    ]

    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_OPCOES, default='Mobilizado')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    empresasecundaria = models.ManyToManyField(
        EmpresaSecundaria,
        related_name='gerentes',
    )

    objects = GerenteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin


    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True