from django.contrib import admin
from gestor.models import Gestor, GestorManager

# Register your models here.
class GestorAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'funcao', 'password', 'status', )
    list_display_links = ('id', 'username', 'email', 'funcao', 'password', 'status',)
    search_fields = ('Nome', 'email', )
    list_filter = ('email', )

    list_per_page = 20


admin.site.register(Gestor, GestorAdmin)