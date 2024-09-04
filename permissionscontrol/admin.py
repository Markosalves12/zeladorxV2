from django.contrib import admin
from permissionscontrol.models import PermissionsJardinagem, PermissionsAccessJardinagem

# Register your models here.
class PermissionsJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'Permissions', )
    list_display_links = ('id', 'Permissions', )

    list_per_page = 20

class PermissionsAccessJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'Gerente', )
    list_display_link = ('id', 'Gerente', )

    list_per_page = 20

admin.site.register(PermissionsJardinagem, PermissionsJardinagemAdmin)
admin.site.register(PermissionsAccessJardinagem, PermissionsAccessJardinagemAdmin)
