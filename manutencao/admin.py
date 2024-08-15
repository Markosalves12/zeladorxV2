from django.contrib import admin
from manutencao.models import MotivoDaManutencao, ManutencaoDeEquipamentos

# Register your models here.
class MotivoDaManutencaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    search_fields = ('nome', 'EmpresaSecundaria', 'status', )
    list_filter = ('nome', 'EmpresaSecundaria', 'status', )

    list_per_page = 20


class ManutencaoDeEquipamentosAdmin(admin.ModelAdmin):
    list_display = ('id', 'Equipamento', 'DataDeInicio', 'DataFim', 'MotivoManutencao', 'Descricaodoservico', )
    list_display_links = ('id', 'Equipamento', 'DataDeInicio', 'DataFim', 'MotivoManutencao', 'Descricaodoservico', )
    search_fields = ('MotivoManutencao', )
    list_filter = ('MotivoManutencao', )

    list_per_page = 20

admin.site.register(ManutencaoDeEquipamentos, ManutencaoDeEquipamentosAdmin)
admin.site.register(MotivoDaManutencao, MotivoDaManutencaoAdmin)