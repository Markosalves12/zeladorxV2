# from django.shortcuts import render, redirect, reverse
# from settings.forms import SettingServicosGestorForms, SettingServicosColaboradorForms
#
#
# # Create your views here.
# def configuracoes_do_gestor(request):
#     forms = SettingServicosGestorForms()
#
#     if request.method == 'POST':
#         form = SettingServicosGestorForms(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('configuracoes_do_gestor')
#
#     return render(
#         request=request,
#         template_name='DataTableAndForms/CreateObject.html',
#         context={
#             'forms': forms,
#             'app_name': 'Gerência de configuração - Gestor',
#             'redirect_close_button': reverse('calendario_jardinagem'),
#             'text_button_save': 'Salvar configuração'
#         }
#     )
#
# def configuracoes_do_colaborador(request):
#     forms = SettingServicosColaboradorForms()
#
#     if request.method == 'POST':
#         form = SettingServicosColaboradorForms(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('configuracoes_do_colaborador')
#
#     return render(
#         request=request,
#         template_name='DataTableAndForms/CreateObject.html',
#         context={
#             'forms': forms,
#             'app_name': 'Gerência de configuração - Colaborador',
#             'redirect_close_button': reverse('calendario_jardinagem'),
#             'text_button_save': 'Salvar configuração'
#         }
#     )

# def configuracoes_do_gestor(request):
#     colunas = [
#         {'nome': 'id', 'label': '#', 'largura': '10px'},
#         {'nome': 'Gestor', 'label': 'Gestor'},
#         {'nome': 'ServicoCompunsivo', 'label': 'Serviços compulsivos'},
#         {'nome': 'TempoPadraoServico', 'label': 'tempo padrão por serviço'},
#         {'nome': 'NotificationToColaboborador', 'label': 'Notificar colaboradores'},
#         {'nome': 'NotificationAceptReject', 'label': 'Notificação de aceitação/rejeição'},
#         {'nome': 'NotificationEndService', 'label': 'Noptificação de fim de serviços'},
#         {'nome': 'NotificationCancelService', 'label': 'Notificação de cancelamento de serviços'},
#         {'nome': 'NotificationNewService', 'label': 'Notificar colaboradores'},
#         {'nome': 'acoes', 'label': 'Ações'},
#     ]
#
#     return generic_view(
#         request=request,
#         model=SettingServicosGestor,
#         form_class=SettingServicosGestorForms,
#         template_name='DataTableAndForms/DataTableAndForms.html',
#         columns=colunas,
#         edition_rout='editar_unidade',
#         app_name='Configurações',
#         text_button_open_modal='Adicionar nova configuração',
#         text_button_save='Salvar configuração',
#         header_model='Nova configuração',
#         redirect_url='configuracoes_do_gestor'
#     )
#
# def editar_configuracao_gestor(request, id_random):
#     return edit_generic_view(
#         request=request,
#         model_class=SettingServicosGestor,
#         form_class=SettingServicosGestorForms,
#         template_name='DataTableAndForms/EditObject.html',
#         id_random=id_random,
#         app_name='Editar configuração',
#         redirect_close_button='configuracoes_do_gestor',
#         redirect_url_name='editar_configuracao_gestor'
#     )