from django.contrib import admin
from colaborador.models import Colaborador

# Register your models here.
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'funcao', 'atividades', 'password', 'status', )
    list_display_links = ('id', 'username', 'email', 'funcao', 'atividades', 'password', 'status', )
    search_fields = ('username', 'email', 'status', )
    list_filter = ('username', 'email', 'status', )

    list_per_page = 20

admin.site.register(Colaborador, ColaboradorAdmin)