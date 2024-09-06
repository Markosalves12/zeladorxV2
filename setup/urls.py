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
    path('admin/', admin.site.urls),
    path('', include('authenticate.urls')),
    # path('', include('colaborador.urls')),
    path('', include('calendario.urls_jardinagem')),
    path('', include('calendario.urls_limpeza_predial')),
    path('', include('unidade.urls')),
    path('', include('localidade.urls')),
    path('', include('areas.urls_jardinagem')),
    path('', include('areas.urls_limpeza_predial')),
    path('', include('empresasecundario.urls')),
    path('', include('catalogo_de_materiais.urls')),
    path('', include('catalogo_de_servicos.urls')),
    path('', include('terrenos.urls')),
    path('', include('vegetacao.urls')),
    # path('', include('gestor.urls')),
    path('', include('gerente.urls')),
    path('', include('servicos.urls_jardinagem')),
    path('', include('servicos.urls_limpeza_predial')),
    path('', include('relatorios.urls')),
    path('', include('dashboards.urls')),
    path('', include('catalogo_de_equipamantos.urls')),
    path('', include('equipamentos.urls')),
    path('', include('manutencao.urls')),
    path('', include('processos.urls')),
    path('', include('settings.urls')),
    path('', include('permissionscontrol.urls_jardinagem')),
    path('', include('history.urls_limpeza_predial')),
    path('', include('history.urls_jardinagem')),
]+static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
