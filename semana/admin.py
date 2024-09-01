from django.contrib import admin
from semana.models import DiasDaSemana

# Register your models here.
class DiasDaSemanaAdmin(admin.ModelAdmin):
    list_display = ('diasdasemana', )


admin.site.register(DiasDaSemana, DiasDaSemanaAdmin)
