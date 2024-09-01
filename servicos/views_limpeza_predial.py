from django.shortcuts import render, redirect, reverse
from servicos.models_limpeza_predial import ServicoLimpezaPredialConfigurado, FatoServicoLimpezaPredial, ServicoLimpezaPredialAgendado
from servicos.forms_limpeza_predial import ServicoLimpezaPredialConfiguradoForms, FatoServicoLimpezaPredialForms, ServicoLimpezaPredialAgendadoForms
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from utils.views import generic_view, edit_generic_view
from colaborador.models import Colaborador
from notifications.utils import enviar_notificacao
from django.utils import timezone


def agendar_servico_limpeza_predial(request):
    forms = ServicoLimpezaPredialAgendadoForms()

    if request.method == 'POST':
        form = ServicoLimpezaPredialAgendadoForms(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('agendar_servico_limpeza_predial')

        print("formulario invalido")

    return render(
        request=request,
        template_name='DataTableAndForms/CreateObject.html',
        context={
            'forms': forms,
            'app_name': 'Agendar serviço de limpeza predial',
            'redirect_close_button': reverse('calendario_limpeza_predial'),
            'redirect_url_name': reverse('agendar_servico_limpeza_predial'),
            'text_button_save': 'Agendar Serviço'
        }
    )

def servicos_agendados_limpeza_predial(request):
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
        {'nome': 'Jardinagem', 'link': reverse('servicos_agendados_jardinagem')},
        {'nome': 'Limpeza predial', 'link': reverse('servicos_agendados_limpeza_predial')}
    ]

    return generic_view(
        request=request,
        model=ServicoLimpezaPredialAgendado,
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name='serviços agendados limpeza predial',
        text_button_open_modal='agendar novo serviço',
        text_button_save='agendar serviço',
        header_model='solicitar serviço',
        redirect_url='servicos_agendados_limpeza_predial',
        link_tipos=tipos
    )

def editar_servico_limpeza_predial_agendado(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=ServicoLimpezaPredialAgendado,
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço',
        redirect_url_name='editar_servico_limpeza_predial_agendado',
        redirect_close_button='servicos_agendados_limpeza_predial'
    )

def configurar_servico_limpeza_predial(request):
    forms = ServicoLimpezaPredialConfiguradoForms()

    if request.method == 'POST':
        form = ServicoLimpezaPredialConfiguradoForms(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            #mensagem de sucesso
            form.save()
            return redirect('configurar_servico_limpeza_predial')

    return render(
        request=request,
        template_name='DataTableAndForms/CreateObject.html',
        context={
            'forms': forms,
            'app_name': 'Configurar serviço de limpeza predial',
            'redirect_close_button': reverse('calendario_limpeza_predial'),
            'redirect_url_name': reverse('configurar_servico_limpeza_predial'),
            'text_button_save': 'Configurar Serviço',
        }
    )

def servicos_configurados_limpeza_predial(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'area', 'label': 'Área'},
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
        {'nome': 'Serviços agendados', 'link': ''},
        {'nome': 'Jardinagem', 'link': ''},
        {'nome': 'Limpeza predial', 'link': reverse('servicos_configurados_limpeza_predial')}
    ]

    return generic_view(
        request=request,
        model=ServicoLimpezaPredialConfigurado,
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
        modal_button=False,
    )


def editar_servico_limpezapredial_configurado(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=ServicoLimpezaPredialConfigurado,
        form_class=ServicoLimpezaPredialConfiguradoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço',
        redirect_url_name='editar_servico_limpezapredial_configurado',
        redirect_close_button='servicos_configurados_limpeza_predial'
    )


def realizar_servico_limpeza_predial_agendado(request, id_random):
    objeto = ServicoLimpezaPredialConfigurado.objects.get(id_random=id_random)
    forms = FatoServicoLimpezaPredialForms(
        instance=objeto,
        id_random_servico=id_random,
        initial={
            'Servico': objeto
        }
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
        }
    )

