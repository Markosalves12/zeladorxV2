from django.contrib import admin
from empresaprimaria.models import EmpresaPrimaria

# Register your models here.
class EmpresaPrimariaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome',  'CNPJ',  'status', )
    list_display_links = ('id', 'nome', 'CNPJ', 'status', )
    search_fields = ('nome', 'CNPJ', )
    list_filter = ('nome', 'CNPJ', )

    list_per_page = 20

admin.site.register(EmpresaPrimaria, EmpresaPrimariaAdmin)