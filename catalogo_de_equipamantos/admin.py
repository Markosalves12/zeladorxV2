from django.contrib import admin
from catalogo_de_equipamantos.models_jardinagem import CatalogoDeEquipamentosJardinagem

# Register your models here.
class CatalogoDeEquipamentosJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    search_fields = ('nome', )
    list_filter = ('nome', )

    list_per_page = 20

admin.site.register(CatalogoDeEquipamentosJardinagem, CatalogoDeEquipamentosJardinagemAdmin)