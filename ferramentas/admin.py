from django.contrib import admin
from ferramentas.models import CatalogoDeFerramentas, FerramentasDisponiveis

# Register your models here.
class CatalogoDeFerramentasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    search_fields = ('nome', )
    list_filter = ('nome', )

    list_per_page = 20

class FerramentasDisponiveisAdmin(admin.ModelAdmin):
    list_display = ('id', 'Nome', 'DataDeAquisicao', 'DataDeDesmobilizacao', 'matricula', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'Nome', 'DataDeAquisicao', 'DataDeDesmobilizacao', 'matricula', 'EmpresaSecundaria', 'status', )
    search_fields = ('Nome', 'DataDeAquisicao', )
    list_filter = ('Nome', )

    list_per_page = 20

admin.site.register(CatalogoDeFerramentas, CatalogoDeFerramentasAdmin)
admin.site.register(FerramentasDisponiveis, FerramentasDisponiveisAdmin)