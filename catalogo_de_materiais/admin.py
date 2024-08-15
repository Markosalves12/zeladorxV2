from django.contrib import admin
from catalogo_de_materiais.models import CatalogoMaterial, ConsumoMateriais, CategoriaMaterial

# Register your models here.
class CatalogoMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    search_fields = ('nome', 'EmpresaSecundaria', 'status', )
    list_filter = ('nome', 'EmpresaSecundaria', 'status', )

    list_per_page = 20


class ConsumoMateriaisAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    search_fields = ('nome', 'EmpresaSecundaria', 'status', )
    list_filter = ('nome', 'EmpresaSecundaria', 'status', )

    list_per_page = 20

class CategoriaMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    search_fields = ('nome', 'EmpresaSecundaria', 'status', )
    list_filter = ('nome', 'EmpresaSecundaria', 'status', )

    list_per_page = 20


admin.site.register(CatalogoMaterial, CatalogoMaterialAdmin)
admin.site.register(ConsumoMateriais, ConsumoMateriaisAdmin)
admin.site.register(CategoriaMaterial, CategoriaMaterialAdmin)