from django.shortcuts import render, redirect, reverse
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from servicos.forms_limpeza_predial import (FatoServicoLimpezaPredialForms,
                                            ServicoLimpezaPredialAgendadoForms)
from utils.views import generic_view, edit_generic_view
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, CharField
from utils.utils import define_range_time

def agendar_servico_limpeza_predial(request, userid):
    forms = ServicoLimpezaPredialAgendadoForms(request=request, userid=userid)

    if request.method == 'POST':
        form = ServicoLimpezaPredialAgendadoForms(request.POST, request.FILES, request=request, userid=userid)
        if form.is_valid():
            form.save()
            messages.info(
                request=request,
                message=f'Serviço(s) '
                        f'{", ".join([str(servico) for servico in form.cleaned_data["ServicosEscalados"].all()])} '
                        f'em {form.cleaned_data["Areas"]} agendado.'
            )

            return redirect('agendar_servico_limpeza_predial', userid)

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

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
        {'nome': 'novo_status', 'label': 'Status'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Serviços agendados', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('servicos_agendados_jardinagem', kwargs={'userid': userid})})

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial', 'link': reverse('servicos_agendados_limpeza_predial', kwargs={'userid': userid})})


    one_day, seven_days = define_range_time()

    return generic_view(
        request=request,
        model=ServicoLimpezaPredialAgendado.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ).annotate(
            novo_status=Case(
                When(status='Em andamento', then=Value('Em andamento')),
                When(DataDeInicio__gte=one_day, DataDeInicio__lt=seven_days, then=Value('Próximo')),
                When(status='Agendado', DataDeInicio__gte=seven_days, then=Value('Agendado')),
                When(DataDeInicio__lt=timezone.now(), then=Value('Atrasado')),
                default=Value('Desconhecido'),
                output_field=CharField()
            )
        ),
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name='serviços agendados limpeza predial',
        form_search=ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
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
        permission_edit=permission_edit,
        url_rehabilitate=reverse(
            'cancelar_servico_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random
            }
        ),
        url_desmobilize=reverse(
            'cancelar_servico_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random
            }
        ),
    )

def realizar_servico_limpeza_predial_agendado(request, userid, id_random):
    objeto = ServicoLimpezaPredialAgendado.objects.get(id_random=id_random)
    forms = FatoServicoLimpezaPredialForms(
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
        form = FatoServicoLimpezaPredialForms(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            objeto.status = 'Em andamento'
            objeto.save()
            messages.success(
                request=request,
                message=f'serviço, {objeto}, realizado'
            )
            return redirect('calendario_limpeza_predial', userid)

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

    return render(
        request=request,
        template_name='DataTableAndForms/EditObject.html',
        context={
            'forms': forms,
            'app_name': 'Realizar serviço',
            'redirect_url_name': 'realizar_servico_limpeza_predial_agendado',
            'id_random': id_random,
            'redirect_close_button': reverse('calendario_limpeza_predial', kwargs={'userid': userid}),
            'text_button': 'Salvar',
            'permission_accompany': permission_accompany
        }
    )

def cancelar_servico_limpeza_predial(request, userid, id_random):
    objeto = ServicoLimpezaPredialAgendado.objects.get(id_random=id_random)
    objeto.status = 'Cancelado'
    objeto.save()

    messages.error(
        request=request,
        message=f'serviço {objeto} cancelado'
    )

    return redirect('calendario_limpeza_predial', userid)


def concluir_servico_limpeza_predial(request, userid, id_random):
    objeto = ServicoLimpezaPredialAgendado.objects.get(id_random=id_random)
    objeto.status = 'Concluido'
    objeto.DataDeConclusao = timezone.now()
    objeto.save()

    messages.success(
        request=request,
        message=f'serviço {objeto} concluido com sucesso'
    )

    return redirect('calendario_limpeza_predial', userid)