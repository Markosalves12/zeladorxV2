from django.shortcuts import get_object_or_404, redirect
from permissionscontrol.models import PermissionsAccessJardinagem, PermissionsJardinagem
from django.core.exceptions import ObjectDoesNotExist
from gerente.models import Gerente

def configurate_permissions(request, model_class, email):
    objeto = get_object_or_404(model_class, email=email)

    permissoes_predefinidas = PermissionsJardinagem.objects.filter(
        id__in=[1, 2, 3]  # IDs das permissões que deseja atribuir automaticamente
    )

    permissions = PermissionsAccessJardinagem(
        Gerente=objeto,
    )
    permissions.save()
    permissions.Permissions.set(permissoes_predefinidas)
    permissions.save()

def validate_permissions(request, userid, permission_to_access):
    try:
        # Buscar as permissões associadas ao gerente com o id fornecido
        permissions_instance = PermissionsAccessJardinagem.objects.get(
            Gerente__id_random=userid
        )
    except:
        permissions_instance = []

    print(type(permissions_instance))

    if isinstance(permissions_instance, PermissionsAccessJardinagem):
        # O objeto encontrado é um queryset (o que não é esperado aqui)
        if len(permissions_instance.Permissions.filter(Permissions__in=permission_to_access)) > 0:
            return True
        else:
            return False

    else:
        return True
