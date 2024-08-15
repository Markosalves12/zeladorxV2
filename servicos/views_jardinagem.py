from django.shortcuts import render, redirect, reverse
from servicos.models_jardinagem import ServicoAgendado
from servicos.forms_jardinagem import ServicoAgendadoForms, FatoServicoForms
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from utils.utils import paginate
from utils.views import generic_view, edit_generic_view
from colaborador.models import Colaborador
from notifications.utils import enviar_notificacao
from django.utils import timezone

# Create your views here.
def agendar_servico(request):
    forms = ServicoAgendadoForms()

    if request.method == 'POST':
        form = ServicoAgendadoForms(request.POST, request.FILES)
        if form.is_valid():
            #mensagem de sucesso
            ColaboradoresEscalados = form.cleaned_data['ColaboradoresEscalados']
            descricao = form.cleaned_data['DescricaoDoServico']
            area = form.cleaned_data['Areas']
            data_inicio = form.cleaned_data['DataDeInicio']
            id_random = form.instance.id_random

            print(id_random)


            for colaborador in ColaboradoresEscalados:
                print(colaborador)

                email = Colaborador.objects.get(
                    id_random=colaborador.id_random
                ).email

                username = Colaborador.objects.get(
                    username=colaborador.username
                ).username

                servicos = list()
                servicos_escalados = form.cleaned_data['ServicosEscalados']
                for servico_cat in servicos_escalados:
                    servicos.append(
                        CatalogodeServicoJardinagem.objects.get(
                            id_random=servico_cat.id_random
                        ).nome
                    )

                enviar_notificacao(
                    destinatario=[email],
                    assunto="Novo serviço",
                    contexto={
                        'id_random': id_random,
                        'colaborador_nome': username,
                        'id_random_colaborador': colaborador.id_random,
                        'descricao': descricao,
                        'area': area,
                        'data_inicio': data_inicio,
                        'servicos': ', '.join(servicos)

                    },
                    template='notifications/new_service.html'
                )


            form.save()
            return redirect('agendar_servico')

    return render(
        request=request,
        template_name='servicos/agendar_servico.html',
        context={
            'forms': forms,
            'app_name': 'Agendar serviço',
            'redirect_close_button': reverse('calendario'),
            'text_button_save': 'Agendar Serviço'
        }
    )

def servicos_agendados(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'ColaboradoresConfirmados', 'label': 'Colaboradores confirmados'},
        {'nome': 'ColaboradoresNegados', 'label': 'Colaboradores negados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'status', 'label': 'Status'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=ServicoAgendado,
        form_class=ServicoAgendado,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_agendado',
        app_name='serviços agendados',
        text_button_open_modal='agendar novo serviço',
        text_button_save='agendar serviço',
        header_model='solicitar serviço',
        redirect_url='servicos_agendados'
    )


def editar_servico_agendado(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=ServicoAgendado,
        form_class=ServicoAgendadoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço',
        redirect_url_name='editar_servico_agendado',
        redirect_close_button='servicos_agendados'
    )


def realizar_servico_agendado(request, id_random):
    objeto = ServicoAgendado.objects.get(id_random=id_random)
    forms = FatoServicoForms(
        instance=objeto,
        id_random_servico=id_random,
        initial={
            'Servico': objeto
        }
    )

    if request.method == 'POST':
        form = FatoServicoForms(request.POST)
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
            'redirect_url_name': 'realizar_servico_agendado',
            'id_random': id_random,
            'redirect_close_button': 'calendario',
            'text_button': 'Salvar',
        }
    )


def cancelar_servico(request, id_random):
    objeto = ServicoAgendado.objects.get(id_random=id_random)
    objeto.status = 'Cancelado'
    objeto.save()

    return redirect('calendario')


def concluir_servico(request, id_random):
    objeto = ServicoAgendado.objects.get(id_random=id_random)
    objeto.status = 'Concluido'
    objeto.DataDeConclusao = timezone.now()
    objeto.save()

    return redirect('calendario')