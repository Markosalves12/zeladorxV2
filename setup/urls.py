"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# imports para trabahar com media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('zeladorxadministration/', admin.site.urls),
    path('', include('authenticate.urls')),
    path('', include('calendario.urls_jardinagem')),
    path('', include('calendario.urls_limpeza_predial')),
    path('', include('unidade.urls')),
    path('', include('localidade.urls_jardinagem')),
    path('', include('localidade.urls_limpeza_predial')),
    path('', include('areas.urls_jardinagem')),
    path('', include('areas.urls_limpeza_predial')),
    path('', include('empresasecundario.urls_jardinagem')),
    path('', include('empresasecundario.urls_limpeza_predial')),

    path('', include('catalogo_de_servicos.urls_jardinagem')),
    path('', include('catalogo_de_servicos.urls_limpeza_predial')),
    path('', include('terrenos.urls')),
    path('', include('vegetacao.urls')),
    path('', include('gerente.urls_jardinagem')),
    path('', include('gerente.urls_limpeza_predial')),

    path('', include('servicos.urls_jardinagem')),
    path('', include('servicos.urls_limpeza_predial')),
    path('', include('servicos.urls_configuracoes_limpeza_predial')),
    path('', include('servicos.urls_configuracoes_jardinagem')),

    path('', include('relatorios.urls_jardinagem')),
    path('', include('relatorios.urls_limpeza_predial')),

    path('', include('dashboards.urls_jardinagem')),
    path('', include('dashboards.urls_limpeza_predial')),

    path('', include('processos.urls')),
    path('', include('settings.urls')),
    path('', include('permissionscontrol.urls_jardinagem')),
    path('', include('permissionscontrol.urls_limpeza_predial')),
    path('', include('permissionscontrol.urls_especials')),
    path('', include('history.urls_limpeza_predial')),
    path('', include('history.urls_jardinagem')),
    path('', include('schedules.urls')),

    path('', include('kanban.urls_jardinagem')),
    path('', include('kanban.urls_limpeza_predial')),

    path('', include('chats.urls')),

    path('', include('checklists.urls_jardinagem')),
    path('', include('checklists.urls_limpeza_predial')),
]+static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)