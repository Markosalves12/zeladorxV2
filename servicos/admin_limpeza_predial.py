from django.contrib import admin
from servicos.models_limpeza_predial import ServicoLimpezaPredial, FatoServicoLimpezaPredial


class ServicoLimpezaPredialAdmin(admin.ModelAdmin):
    list_display = ('ServicosEscalados', 'horario_1', 'horario_2', 'horario_3', 'horario_4', 'horario_5', 'horario_6',
                    'horario_7', 'horario_8', 'horario_9',)
    list_display_links = ('ServicosEscalados', 'horario_1', 'horario_2', 'horario_3', 'horario_4', 'horario_5', 'horario_6',
                    'horario_7', 'horario_8', 'horario_9',)
    search_fields = ('ServicosEscalados', )
    list_filter = ('ServicosEscalados', )

    list_per_page = 20

class FatoServicoLimpezaPredialAdmin(admin.ModelAdmin):
    list_display = ('Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Colaborador', )
    list_display_links = ('Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Colaborador', )
    search_fields = ('Servico',  )
    list_filter = ('Servico', )

    list_per_page = 20


admin.site.register(ServicoLimpezaPredial, ServicoLimpezaPredialAdmin)
admin.site.register(FatoServicoLimpezaPredial, FatoServicoLimpezaPredialAdmin)