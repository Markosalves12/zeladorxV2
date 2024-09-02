from django.shortcuts import get_object_or_404
from permissionscontrol.models import PermissionsAccessJardinagem, PermissionsJardinagem
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