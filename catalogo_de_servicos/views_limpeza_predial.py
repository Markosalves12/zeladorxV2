from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from catalogo_de_servicos.forms_limpeza_predial import CatalogoServicoLimpezaPredialForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status
from django.shortcuts import reverse, redirect
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas
from django.contrib import messages


# Create your views here.
def catalogo_de_servicos_limpeza_predial(request, userid):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Catálogo de serviços', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('catalogo_de_servicos_jardinagem', kwargs={'userid': userid})})

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial', 'link': reverse('catalogo_de_servicos_limpeza_predial', kwargs={'userid': userid})})
    else:
        return redirect('catalogo_de_servicos_jardinagem', userid)

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['262: Pode visualizar serviços do catálogo']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['261: Pode editar serviços do catálogo']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['260: Pode criar novos serviços ao catálogo']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    return generic_view(
        request=request,
        model=CatalogodeServicoLimpezaPredial.objects.filter(
            EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            EmpresaSecundaria__id_random__in=empresas_secundarias_ids
        ),
        form_class=CatalogoServicoLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_catalogo_de_servicos_limpeza_predial',
        history_rout='historico_de_servicos_catologo_de_servicos_limpeza_predial',
        app_name='catálogo de serviços limpeza predial',
        form_search=CatalogoServicoLimpezaPredialForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'EmpresaSecundaria': 'EmpresaSecundaria__id',
        },
        text_button_open_modal='Adicionar novo serviço',
        text_button_save='Salvar serviço',
        header_model='Novo serviço',
        redirect_url='catalogo_de_servicos_limpeza_predial',
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )

def editar_catalogo_de_servicos_limpeza_predial(request, userid, id_random):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['261: Pode editar serviços do catálogo']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['263: Pode excluir serviços do catálogo']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['264: Pode desmobilizar serviços do catálogo']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['265: Pode reabilitar serviços do catálogo']
    )

    return edit_generic_view(
        request=request,
        model_class=CatalogodeServicoLimpezaPredial,
        form_class=CatalogoServicoLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço do catálogo de limpeza predial',
        redirect_url_name='editar_catalogo_de_servicos_limpeza_predial',
        redirect_close_button=reverse('catalogo_de_servicos_limpeza_predial', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
        url_desmobilize=reverse(
            'alterar_status_catalogo_de_servicos_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_catalogo_de_servicos_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
    )

def alterar_status_catalogo_de_servicos_limpeza_predial(request, userid, id_random, new_status):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    objeto = CatalogodeServicoLimpezaPredial.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=CatalogodeServicoLimpezaPredial,
        redirect_url_name=reverse('editar_catalogo_de_servicos_limpeza_predial', kwargs={'userid': userid, 'id_random': id_random}),
        id_random=id_random,
        new_status=new_status,
        message=f'{objeto.nome} reabilitado com sucesso' if new_status == 'Mobilizado' else f'{objeto.nome} desmobilizado com sucesso'
    )