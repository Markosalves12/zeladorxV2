from django.shortcuts import render, redirect, reverse
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions
from utils.views import generic_view, GenericIfDeleteView, GenericDeleteView
from solicitacoes.models import QRCodeAreaJardinagem
from solicitacoes.forms_jardinagem import QRCodeAreaJardinagemForms


# Create your views here.
def qr_codes_jardinagem(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Tipo de solicitação', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('qr_codes_jardinagem', kwargs={'userid': userid})})
    else:
        return redirect('qr_codes_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2,
                     {'nome': 'Limpeza predial', 'link': reverse('qr_codes_limpeza_predial', kwargs={'userid': userid})})

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['252: Pode visualizar áreas de jardinagem']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['251: Pode editar áreas de jardinagem']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['250: Pode criar novas áreas de jardinagem']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Areas', 'label': 'Área'},
        {'nome': 'codigo', 'label': 'Código'},
        {'nome': 'imagem_qr', 'label': 'QR código'},
    ]

    return generic_view(
        request=request,
        model=QRCodeAreaJardinagem.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ).distinct(),
        form_class=QRCodeAreaJardinagemForms,
        template_name='DataTableAndForms/ViewQRcodes.html',
        columns=colunas,
        edition_rout='editar_area_jardins',
        history_rout='historico_de_servicos_areas_jardinagem',
        app_name='QR Codes disponiveis',
        form_search=QRCodeAreaJardinagemForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
        },
        text_button_open_modal='Criar QR code',
        text_button_save='Salvar QR',
        header_model='Nova código QR',
        redirect_url=reverse('qr_codes_jardinagem', kwargs={'userid': userid}),
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid,
    )



def IfDeleteQRCodeJardinagem(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=QRCodeAreaJardinagem,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['253: Pode excluir áreas de jardinagem'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar QR code jardinagem",
        url_delete=reverse(
            'DeleteQRCodeJardinagem',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('qr_codes_jardinagem', kwargs={'userid': request.user.id_random})
    )



def DeleteQRCodeJardinagem(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=QRCodeAreaJardinagem,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['253: Pode excluir áreas de jardinagem'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        redirect_close_button=reverse('qr_codes_jardinagem', kwargs={'userid': request.user.id_random}),
    )