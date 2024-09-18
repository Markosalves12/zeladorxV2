from django.shortcuts import render, redirect, reverse
from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms, FatoServicoJardinagemForms
# from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from utils.views import generic_view, edit_generic_view
# from gerente.models import Gerente
# from notifications.utils import enviar_notificacao
from django.utils import timezone
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def agendar_servico_jardinagem(request, userid):
    forms = ServicoJaridinagemAgendadoForms(request=request, userid=userid)

    if request.method == 'POST':
        form = ServicoJaridinagemAgendadoForms(request.POST, request.FILES, request=request, userid=userid)
        if form.is_valid():
            form.save()
            return redirect('agendar_servico_jardinagem', userid)

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
            'app_name': 'Agendar serviço de jardinagem',
            'redirect_close_button': reverse('calendario_jardinagem', kwargs={'userid': userid}),
            'redirect_url_name': reverse('agendar_servico_jardinagem', kwargs={'userid': userid}),
            'text_button_save': 'Agendar Serviço',
            "link_tipos": tipos
        }
    )

def servicos_agendados_jardinagem(request, userid):
    # ('323: Pode excluir serviços agendados', '323: Pode excluir serviços agendados'),
    # ('324: Pode acompanhar serviços agendados', '324: Pode acompanhar serviços agendados'),
    # ('325: Pode editar serviços em andamento', '325: Pode editar serviços em andamento'),
    # ('326 Pode concluir serviços em andamento', '326: Pode concluir serviços em andamento'),
    # ('327 Pode excluir serviços concluidos', '327: Pode excluir serviços concluidos'),

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['322: Pode visualizar serviços agendados']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['321: Pode editar serviços agendados']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['320: Pode agendar novos serviços']
    )

    colunas = [
        {'nome': 'id','label': '#','largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'ColaboradoresConfirmados', 'label': 'Colaboradores confirmados'},
        {'nome': 'ColaboradoresNegados', 'label': 'Colaboradores negados'},
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
        model=ServicoJardinagemAgendado.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ),
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='serviços agendados jardinagem',
        text_button_open_modal='agendar novo serviço',
        text_button_save='agendar serviço',
        header_model='solicitar serviço',
        redirect_url='servicos_agendados_jardinagem',
        link_tipos=tipos,
        permission_crate=permission_crate,
        permission_view=permission_view,
        permission_edit=permission_edit,
        userid=userid
    )


def editar_servico_jardinagem_agendado(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['321: Pode editar serviços agendados']
    )

    return edit_generic_view(
        request=request,
        model_class=ServicoJardinagemAgendado,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço',
        redirect_url_name='editar_servico_jardinagem_agendado',
        redirect_close_button=reverse('servicos_agendados_jardinagem', kwargs={'userid': userid}),
        permission_edit=permission_edit
    )


def realizar_servico_jardinagem_agendado(request, userid, id_random):
    objeto = ServicoJardinagemAgendado.objects.get(id_random=id_random)
    forms = FatoServicoJardinagemForms(
        instance=objeto,
        id_random=id_random,
        initial={
            'Servico': objeto
        },
        request=request,
        userid=userid
    )

    permission_accompany = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['324: Pode acompanhar serviços agendados']
    )

    if request.method == 'POST':
        form = FatoServicoJardinagemForms(request.POST, request.FILES, request=request, userid=userid)
        print(form.errors)
        if form.is_valid():
            form.save()
            objeto.status = 'Em andamento'
            objeto.save()
            return redirect('calendario_jardinagem', userid)


    return render(
        request=request,
        template_name='DataTableAndForms/EditObject.html',
        context={
            'forms': forms,
            'app_name': 'Realizar serviço',
            'redirect_url_name': 'realizar_servico_jardinagem_agendado',
            'id_random': id_random,
            'redirect_close_button': reverse('calendario_jardinagem', kwargs={'userid': userid}),
            'text_button': 'Salvar',
            'permission_accompany': permission_accompany
        }
    )


def cancelar_servico_jardinagem(request, userid, id_random):
    objeto = ServicoJardinagemAgendado.objects.get(id_random=id_random)
    objeto.status = 'Cancelado'
    objeto.save()

    return redirect('calendario_jardinagem', userid)


def concluir_servico_jardinagem(request, userid, id_random):
    objeto = ServicoJardinagemAgendado.objects.get(id_random=id_random)
    objeto.status = 'Concluido'
    objeto.DataDeConclusao = timezone.now()
    objeto.save()

    return redirect('calendario_jardinagem', userid)