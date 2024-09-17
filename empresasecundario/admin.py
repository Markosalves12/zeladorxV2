from django.contrib import admin
from empresasecundario.models import EmpresaSecundaria

# Register your models here.
class EmpresaSecundariaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'CNPJ', 'status', 'empresaprimaria', )
    list_display_links = ('id', 'nome', 'CNPJ', 'status', 'empresaprimaria', )
    search_fields = ('nome', 'CNPJ', )
    list_filter = ('nome', 'CNPJ', )

    list_per_page = 20

admin.site.register(EmpresaSecundaria, EmpresaSecundariaAdmin)