from django.contrib import admin
from empresasecundario.models import EmpresaSecundaria

# Register your models here.
class EmpresaSecundariaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'CNPJ', 'status', 'setor', 'empresaprimaria', )
    list_display_links = ('id', 'nome', 'CNPJ', 'status', 'setor', 'empresaprimaria', )
    search_fields = ('setor', 'nome', 'CNPJ', )
    list_filter = ('setor', 'nome', 'CNPJ', )

    list_per_page = 20

admin.site.register(EmpresaSecundaria, EmpresaSecundariaAdmin)