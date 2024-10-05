from django.shortcuts import render, redirect, reverse
from servicos.models_jardinagem import ServicoJardinagemConfigurado
from servicos.forms_configuracoes_jardinagem import ServicoJardinagemConfiguradoForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status, generic_view_history
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas
from django.contrib import messages
from servicos.models_jardinagem import ServicoJardinagemAgendado
from utils.utils import paginate


def configurar_servico_jardinagem(request, userid):
    forms = ServicoJardinagemConfiguradoForms(request=request, userid=userid)

    if request.method == 'POST':
        form = ServicoJardinagemConfiguradoForms(request.POST, request.FILES, request=request, userid=userid)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.info(
                request=request,
                message=f'Serviço(s) '
                        f'{", ".join([str(servico) for servico in form.cleaned_data["ServicosEscalados"].all()])} '
                        f'em {form.cleaned_data["Areas"]}, configurado.'
            )

            return redirect('configurar_servico_jardinagem', userid)

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

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
        {'nome': 'diasaseremrealizado', 'label': 'Dias a serem realizados'},
        {'nome': 'horario_1', 'label': 'Horario 1'},
        {'nome': 'horario_2', 'label': 'Horario 2'},
        {'nome': 'horario_3', 'label': 'Horario 3'},
        {'nome': 'horario_4', 'label': 'Horario 4'},
        {'nome': 'horario_5', 'label': 'Horario 5'},
        {'nome': 'horario_6', 'label': 'Horario 6'},
        {'nome': 'horario_7', 'label': 'Horario 7'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Serviços Configurados', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('servicos_configurados_jardinagem', kwargs={'userid': userid})},)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial', 'link': reverse('servicos_configurados_limpeza_predial', kwargs={'userid': userid})})

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
        history_rout='historico_de_servicos_configurados_jardinagem',
        app_name='serviços configurados jardinagem',
        form_search=ServicoJardinagemConfiguradoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'diasaseremrealizado': 'diasaseremrealizado'
        },
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
        permission_edit=permission_edit,
        permission_exclude=True,
        permission_desmobilize=True,
        permission_rehabilitate=True,
        url_desmobilize=reverse(
            'alterar_status_servico_jardinagem_configurado',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_servico_jardinagem_configurado',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
    )


def alterar_status_servico_jardinagem_configurado(request, userid, id_random, new_status):
    objeto = ServicoJardinagemConfigurado.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=ServicoJardinagemConfigurado,
        redirect_url_name=reverse(
            'editar_servico_jardinagem_configurado',
            kwargs={
                'userid': userid,
                'id_random': id_random
            }
        ),
        id_random=id_random,
        new_status=new_status,
        message=f'{objeto} reabilitado com sucesso' if new_status == 'Mobilizado' else f'{objeto} desmobilizado com sucesso'
    )


def historico_de_servicos_configurados_jardinagem(request, userid, id_random):
    objeto = ServicoJardinagemConfigurado.objects.get(
        id_random=id_random
    )

    objetos = ServicoJardinagemAgendado.objects.filter(
        id_configuracao=id_random,
        status__in=['Concluido']
    )

    return generic_view_history(
        request=request,
        userid=userid,
        id_random=id_random,
        app_name=f'Histórico de serviços {objeto}',
        objeto=objeto,
        objetos=objetos,
        type_exibition='jardinagem_agendado',
        type_export='configuracao',
        form_search=ServicoJardinagemConfiguradoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'diasaseremrealizado': 'diasaseremrealizado'
        },
        export_pdf='exportar_relatorio_de_serivos_na_area_jardinagem_pdf',
        export_excel='exportar_relatorio_de_serivos_na_area_Jardinagem_excel',
        foto_objeto=None,
        Foto=False,
        redirect_close_button='servicos_configurados_jardinagem'
    )