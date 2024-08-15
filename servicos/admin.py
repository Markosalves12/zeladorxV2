from django.contrib import admin
from servicos.models_jardinagem import ServicoAgendado, FatoServico

# Register your models here.
class ServicoAgendadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'DataDeInicio', 'DescricaoDoServico', 'Areas', 'status', 'foto_solicitacao', 'foto_entrega', 'DataDeConclusao',)
    list_display_links = ('id', 'DataDeInicio', 'DescricaoDoServico', 'Areas', 'status', 'foto_solicitacao', 'foto_entrega', 'DataDeConclusao',)
    search_fields = ('DataDeInicio', 'status', 'DataDeConclusao', )
    list_filter = ('status', )

    list_per_page = 20

class FatoServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'Servico', 'data_hora_chegada_na_area', 'EquipamentoUsado', 'data_hora_retorno_area', 'Colaborador',)
    list_display_links = ('id', 'Servico', 'data_hora_chegada_na_area', 'EquipamentoUsado', 'data_hora_retorno_area', 'Colaborador',)
    search_fields = ('Servico', 'data_hora_chegada_na_area', 'EquipamentoUsado', 'data_hora_retorno_area', 'Colaborador',)
    list_filter = ('Colaborador', )

    list_per_page = 20


admin.site.register(FatoServico, FatoServicoAdmin)
admin.site.register(ServicoAgendado, ServicoAgendadoAdmin)
