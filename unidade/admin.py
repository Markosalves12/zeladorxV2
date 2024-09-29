from django.contrib import admin
from unidade.models import Unidade

# Register your models here.
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'linkmapajardinagem','linkmapalimnpezapredial', 'foto', 'status',)
    list_display_links = ('id', 'nome', 'linkmapajardinagem', 'linkmapalimnpezapredial', 'foto', 'status',)
    search_fields = ('nome',  'status', )
    list_filter = ('nome',  'status', )

    list_per_page = 20


admin.site.register(Unidade, UnidadeAdmin)