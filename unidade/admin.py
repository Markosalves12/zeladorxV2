from django.contrib import admin
from unidade.models import Unidade

# Register your models here.
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'linkmapa', 'foto', 'EmpresaSecundaria', 'status',)
    list_display_links = ('id', 'nome', 'linkmapa', 'foto', 'EmpresaSecundaria', 'status',)
    search_fields = ('nome', 'EmpresaSecundaria', 'status', )
    list_filter = ('nome', 'EmpresaSecundaria', 'status', )

    list_per_page = 20


admin.site.register(Unidade, UnidadeAdmin)