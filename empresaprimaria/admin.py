from django.contrib import admin
from empresaprimaria.models import EmpresaPrimaria

# Register your models here.
class EmpresaPrimariaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'razao_social', 'CNPJ', 'username', 'password', 'status', )
    list_display_links = ('id', 'nome', 'razao_social', 'CNPJ', 'username', 'password', 'status', )
    search_fields = ('username', 'nome', 'CNPJ', )
    list_filter = ('username', 'nome', 'CNPJ', )

    list_per_page = 20

admin.site.register(EmpresaPrimaria, EmpresaPrimariaAdmin)