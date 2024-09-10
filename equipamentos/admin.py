from django.contrib import admin
from equipamentos.models_jardinagem import EquipamentoDisponiveisJardinagem

# Register your models here.
class EquipamentoDisponiveisJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'Nome', 'DataDeAquisicao', 'DataDeDesmobilizacao', 'matricula', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'Nome', 'DataDeAquisicao', 'DataDeDesmobilizacao', 'matricula', 'EmpresaSecundaria', 'status', )
    search_fields = ('Nome', 'DataDeAquisicao', )
    list_filter = ('Nome', )

    list_per_page = 20

admin.site.register(EquipamentoDisponiveisJardinagem, EquipamentoDisponiveisJardinagemAdmin)