from django.shortcuts import render, redirect, reverse
from servicos.models_limpeza_predial import ServicoLimpezaPredialConfigurado, ServicoLimpezaPredialAgendado
from servicos.forms_limpeza_predial import ServicoLimpezaPredialConfiguradoForms, FatoServicoLimpezaPredialForms, ServicoLimpezaPredialAgendadoForms
from utils.views import generic_view, edit_generic_view
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

def agendar_servico_limpeza_predial(request, userid):
    forms = ServicoLimpezaPredialAgendadoForms(request=request, userid=userid)

    if request.method == 'POST':
        form = ServicoLimpezaPredialAgendadoForms(request.POST, request.FILES, request=request, userid=userid)
        if form.is_valid():
            form.save()
            return redirect('agendar_servico_limpeza_predial', userid)

    tipos = [
        {'nome': 'Agendar serviços', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('agendar_servico_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('agendar_servico_limpeza_predial', kwargs={'userid': userid})},
    ]

    return render(
        request=request,
        template_name='DataTableAndForms/CreateObject.html',
        context={
            'forms': forms,
            'app_name': 'Agendar serviço de limpeza predial',
            'redirect_close_button': reverse('calendario_limpeza_predial', kwargs={'userid': userid}),
            'redirect_url_name': reverse('agendar_servico_limpeza_predial', kwargs={'userid': userid}),
            'text_button_save': 'Agendar Serviço',
            "link_tipos": tipos
        }
    )

def servicos_agendados_limpeza_predial(request, userid):
    # ('323: Pode excluir serviços agendados', '323: Pode excluir serviços agendados'),
    # ('324: Pode acompanhar serviços agendados', '324: Pode acompanhar serviços agendados'),
    # ('325: Pode editar serviços em andamento', '325: Pode editar serviços em andamento'),
    # ('326 Pode concluir serviços em andamento', '326: Pode concluir serviços em andamento'),
    # ('327 Pode excluir serviços concluidos', '327: Pode excluir serviços concluidos'),

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['322: Pode visualizar serviços agendados']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['321: Pode editar serviços agendados']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['320: Pode agendar novos serviços']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'status', 'label': 'Status'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    tipos = [
        {'nome': 'Serviços agendados', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('servicos_agendados_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('servicos_agendados_limpeza_predial', kwargs={'userid': userid})},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=ServicoLimpezaPredialAgendado.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ),
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name='serviços agendados limpeza predial',
        text_button_open_modal='agendar novo serviço',
        text_button_save='agendar serviço',
        header_model='solicitar serviço',
        redirect_url='servicos_agendados_limpeza_predial',
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )

def editar_servico_limpeza_predial_agendado(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['321: Pode editar serviços agendados']
    )

    return edit_generic_view(
        request=request,
        model_class=ServicoLimpezaPredialAgendado,
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço',
        redirect_url_name='editar_servico_limpeza_predial_agendado',
        redirect_close_button=reverse('servicos_agendados_limpeza_predial', kwargs={'userid': userid}),
        permission_edit=permission_edit
    )

def configurar_servico_limpeza_predial(request, userid):
    forms = ServicoLimpezaPredialConfiguradoForms(request=request, userid=userid)

    if request.method == 'POST':
        form = ServicoLimpezaPredialConfiguradoForms(request.POST, request.FILES, request=request, userid=userid)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('configurar_servico_limpeza_predial')

    tipos = [
        {'nome': 'Configurar serviços', 'link': ''},
        {'nome': 'Jardinagem', 'link': ''},
        {'nome': 'Limpeza predial', 'link': reverse('configurar_servico_limpeza_predial', kwargs={'userid': userid})},
    ]

    return render(
        request=request,
        template_name='DataTableAndForms/CreateObject.html',
        context={
            'forms': forms,
            'app_name': 'Configurar serviço de limpeza predial',
            'redirect_close_button': reverse('calendario_limpeza_predial', kwargs={'userid': userid}),
            'redirect_url_name': reverse('configurar_servico_limpeza_predial', kwargs={'userid': userid}),
            'text_button_save': 'Configurar Serviço',
            'link_tipos': tipos
        }
    )

def servicos_configurados_limpeza_predial(request, userid):
    # ('373: Pode excluir serviços configurados', '373: Pode excluir serviços configurados'),
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['372: Pode visualizar serviços configurados']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['371: Pode editar serviços configurados']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
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
        {'nome': 'Jardinagem', 'link': ''},
        {'nome': 'Limpeza predial', 'link': reverse('servicos_configurados_limpeza_predial', kwargs={'userid': userid})}
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=ServicoLimpezaPredialConfigurado.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ),
        form_class=ServicoLimpezaPredialConfiguradoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpezapredial_configurado',
        app_name='serviços configurados limpeza predial',
        text_button_open_modal='configurar novo serviço',
        text_button_save='configurar serviço',
        header_model='solicitar serviço',
        redirect_url='servicos_configurados_limpeza_predial',
        link_tipos=tipos,
        userid=userid,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        permission_view=permission_view
    )


def editar_servico_limpezapredial_configurado(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['371: Pode editar serviços configurados']
    )

    return edit_generic_view(
        request=request,
        model_class=ServicoLimpezaPredialConfigurado,
        form_class=ServicoLimpezaPredialConfiguradoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço',
        redirect_url_name='editar_servico_limpezapredial_configurado',
        redirect_close_button=reverse('servicos_configurados_limpeza_predial', kwargs={'userid': userid}),
        permission_edit=permission_edit
    )


def realizar_servico_limpeza_predial_agendado(request, userid, id_random):
    objeto = ServicoLimpezaPredialAgendado.objects.get(id_random=id_random)
    forms = FatoServicoLimpezaPredialForms(
        instance=objeto,
        initial={
            'Servico': objeto
        }
    )

    permission_accompany = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['324: Pode acompanhar serviços agendados']
    )

    if request.method == 'POST':
        form = ServicoLimpezaPredialConfiguradoForms(request.POST)
        if form.is_valid():
            form.save()
            objeto.status = 'Em andamento'
            objeto.save()
            return redirect('calendario')


    return render(
        request=request,
        template_name='DataTableAndForms/EditObject.html',
        context={
            'forms': forms,
            'app_name': 'Realizar serviço',
            'redirect_url_name': 'realizar_servico_jardinagem_agendado',
            'id_random': id_random,
            'redirect_close_button': 'calendario',
            'text_button': 'Salvar',
            'permission_accompany': permission_accompany
        }
    )