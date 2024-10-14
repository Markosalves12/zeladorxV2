# Create your views here.
from django.shortcuts import reverse, redirect
from gerente.models import Gerente
from gerente.forms_limpeza_predial import GerenteLimpezaPredialForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status, generic_view_history
from permissionscontrol.utils import validate_permissions, verify_login
from empresasecundario.utils import define_empresas
from servicos.utils_limpeza_predial import colect_dados_fato_servico_limpeza_predial
from servicos.forms_limpeza_predial import ServicoLimpezaPredialAgendadoForms


# Create your views here.
def gerentes_limpeza_predial(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Gerentes', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('gerentes_jardinagem', kwargs={'userid': userid})})

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial',
                         'link': reverse('gerentes_limpeza_predial', kwargs={'userid': userid})})
    else:
        redirect('gerentes_jardinagem', userid)

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['282: Pode visualizar colaboradores']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['281: Pode editar colaboradores']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['280: Pode criar novos colaboradores']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'username', 'label': 'Nome'},
        {'nome': 'email', 'label': 'E-mail'},
        {'nome': 'empresasecundaria', 'label': 'Empresa(s)'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    return generic_view(
        request=request,
        model=Gerente.objects.filter(
            empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            empresasecundaria__id_random__in=empresas_secundarias_ids,
            empresasecundaria__setor__setor='Limpeza predial'
        ).distinct(),
        form_class=GerenteLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_gerente_limpeza_predial',
        history_rout='historico_de_servicos_gerente_limpeza_predial',
        app_name='gerentes limpeza predial',
        form_search=GerenteLimpezaPredialForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'email': 'email',
            'username': 'username',
            'empresasecundaria': 'empresasecundaria__id'
        },
        text_button_open_modal='Adicionar novo gerente',
        text_button_save='Salvar gerente',
        header_model='Novo gerente',
        redirect_url='gerentes_limpeza_predial',
        configurate_gerente=True,
        link_tipos=tipos,
        userid=userid,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate
    )


def editar_gerente_limpeza_predial(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['281: Pode editar colaboradores']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['283: Pode excluir colaboradores']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['284: Pode desmobilizar colaboradores']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['285: Pode reabilitar colaboradores']
    )

    return edit_generic_view(
        request=request,
        model_class=Gerente,
        form_class=GerenteLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar gerente',
        redirect_url_name='editar_gerente_limpeza_predial',
        redirect_close_button=reverse('gerentes_limpeza_predial', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
        url_desmobilize=reverse(
            'alterar_status_gerente_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_gerente_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
    )


def alterar_status_gerente_limpeza_predial(request, userid, id_random, new_status):
    objeto = Gerente.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=Gerente,
        redirect_url_name=reverse('editar_gerente_limpeza_predial', kwargs={'userid': userid, 'id_random': id_random}),
        id_random=id_random,
        new_status=new_status,
        message=f'{objeto.username} reabilitado com sucesso' if new_status == 'Mobilizado' else f'{objeto.username} desmobilizado com sucesso'
    )


def historico_de_servicos_gerente_limpeza_predial(request, userid, id_random):
    permission_extract_pdf = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['311: Pode extrair relatórios PDF de limpeza predial']
    )

    permission_extract_xlsx = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['310: Pode extrair relatórios XLSX de limpeza predial']
    )

    objeto = Gerente.objects.get(
        id_random=id_random
    )

    objetos = colect_dados_fato_servico_limpeza_predial(
        request=request,
        userid=userid,
        DataDeInicio='None',
        DataDeConclusao='None',
        TipoServico='None',
        Areas='None',
        ServicosEscalados=['None'],
        ColaboradoresEscalados=['None'],
        status=['Concluido'],
    ).filter(
        colaborador_envolvido_id_random=id_random
    )

    return generic_view_history(
        request=request,
        userid=userid,
        id_random=id_random,
        app_name=f'Histórico de serviços {objeto.username}',
        objeto=objeto,
        objetos=objetos,
        type_exibition='fato_jardinagem',
        type_export='gerente',
        form_search=ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'TipoServico': 'tipo_de_servico',
            'ServicosEscalados': 'servicos_solicitados_id',
            'DataDeInicio': 'data_de_inicio',
            'DataDeConclusao': 'data_de_conclusao',
            'Areas': 'area_atendid_id'
        },
        export_pdf='exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf',
        export_excel='exportar_relatorio_de_serivos_na_area_limpeza_predial_excel',
        foto_objeto=None,
        Foto=False,
        redirect_close_button='gerentes_limpeza_predial',
        permission_extract_pdf=permission_extract_pdf,
        permission_extract_xlsx=permission_extract_xlsx
    )
