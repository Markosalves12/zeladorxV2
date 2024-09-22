from django.shortcuts import render, redirect, reverse
from servicos.models_jardinagem import ServicoJardinagemConfigurado
from servicos.forms_configuracoes_jardinagem import ServicoJardinagemConfiguradoForms
from utils.views import generic_view, edit_generic_view
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

def configurar_servico_jardinagem(request, userid):
    forms = ServicoJardinagemConfiguradoForms(request=request, userid=userid)

    if request.method == 'POST':
        form = ServicoJardinagemConfiguradoForms(request.POST, request.FILES, request=request, userid=userid)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('configurar_servico_jardinagem', userid)

    tipos = [
        {'nome': 'Configurar serviços', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('configurar_servico_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('configurar_servico_limpeza_predial', kwargs={'userid': userid})},
    ]

    return render(
        request=request,
        template_name='DataTableAndForms/CreateObject.html',
        context={
            'forms': forms,
            'app_name': 'Configurar serviço de jardinagem',
            'redirect_close_button': reverse('calendario_jardinagem', kwargs={'userid': userid}),
            'redirect_url_name': reverse('configurar_servico_jardinagem', kwargs={'userid': userid}),
            'text_button_save': 'Configurar Serviço',
            'link_tipos': tipos
        }
    )

def servicos_configurados_jardinagem(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['372: Pode visualizar serviços configurados']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['371: Pode editar serviços configurados']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['370: Pode configurar novos serviços']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Areas', 'label': 'Área'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'tempomedioplanejado', 'label': 'Tempo médio planejado'},
        {'nome': 'horario_1', 'label': 'Horario 1'},
        {'nome': 'horario_2', 'label': 'Horario 2'},
        {'nome': 'horario_3', 'label': 'Horario 3'},
        {'nome': 'horario_4', 'label': 'Horario 4'},
        {'nome': 'horario_5', 'label': 'Horario 5'},
        {'nome': 'horario_6', 'label': 'Horario 6'},
        {'nome': 'horario_7', 'label': 'Horario 7'},
        {'nome': 'horario_8', 'label': 'Horario 8'},
        {'nome': 'horario_9', 'label': 'Horario 9'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    tipos = [
        {'nome': 'Serviços Configurados', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('servicos_configurados_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('servicos_configurados_limpeza_predial', kwargs={'userid': userid})}
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=ServicoJardinagemConfigurado.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ),
        form_class=ServicoJardinagemConfiguradoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_configurado',
        app_name='serviços configurados jardinagem',
        text_button_open_modal='configurar novo serviço',
        text_button_save='configurar serviço',
        header_model='solicitar serviço',
        redirect_url='servicos_configurados_jardinagem',
        link_tipos=tipos,
        userid=userid,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        permission_view=permission_view
    )


def editar_servico_jardinagem_configurado(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['371: Pode editar serviços configurados']
    )

    return edit_generic_view(
        request=request,
        model_class=ServicoJardinagemConfigurado,
        form_class=ServicoJardinagemConfiguradoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço',
        redirect_url_name='editar_servico_jardinagem_configurado',
        redirect_close_button=reverse('servicos_configurados_jardinagem', kwargs={'userid': userid}),
        permission_edit=permission_edit
    )