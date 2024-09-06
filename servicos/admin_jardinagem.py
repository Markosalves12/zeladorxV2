from django.contrib import admin

# Register your models here.
class ServicoJardinagemAgendadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'DataDeInicio', 'DescricaoDoServico', 'Areas', 'status', 'foto_solicitacao', 'foto_entrega', 'DataDeConclusao',)
    list_display_links = ('id', 'DataDeInicio', 'DescricaoDoServico', 'Areas', 'status', 'foto_solicitacao', 'foto_entrega', 'DataDeConclusao',)
    search_fields = ('DataDeInicio', 'status', 'DataDeConclusao', )
    list_filter = ('status', )

    list_per_page = 20

class FatoServicoJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'Servico', 'data_hora_chegada_na_area', 'EquipamentoUsado', 'data_hora_retorno_area', 'Gerente',)
    list_display_links = ('id', 'Servico', 'data_hora_chegada_na_area', 'EquipamentoUsado', 'data_hora_retorno_area', 'Gerente',)
    search_fields = ('Servico', 'data_hora_chegada_na_area', 'EquipamentoUsado', 'data_hora_retorno_area', 'Colaborador',)
    list_filter = ('Gerente', )

    list_per_page = 20


