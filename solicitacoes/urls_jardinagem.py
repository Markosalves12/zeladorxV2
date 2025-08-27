from django.urls import path
from solicitacoes.views_jardinagem import (solicitacoes_jardinagem, solicitar_servico_jardinagem,
                                           editar_solicitacao_jardinagem, accept_solicitacao_jardinagem,
                                           confirm_solicitacao_jardinagem, reject_solicitacao_jardinagem)
from solicitacoes.views_qr_codes_jardinagem import qr_codes_jardinagem, IfDeleteQRCodeJardinagem, DeleteQRCodeJardinagem
from solicitacoes.views_export_qr_codes_jardinagem import exportar_qr_code_jardinagem_png, exportar_qr_code_jardinagem_pdf

urlpatterns = [
    path(
        'solicitacoes-servico-jardinagem/<str:userid>/',
         solicitacoes_jardinagem,
         name='solicitacoes_jardinagem'
    ),
    path(
        'qr-codes-jardinagem/<str:userid>/',
        qr_codes_jardinagem,
        name='qr_codes_jardinagem'
    ),

    path(
        'solicitar-servico-jardinagem/<str:id_randomqr>/<str:id_randomarea>/',
        solicitar_servico_jardinagem,
        name='solicitar_servico_jardinagem'
    ),
    path(
        'editar-solicitacao-jardinagem/<str:userid>/<str:id_random>/',
        editar_solicitacao_jardinagem,
        name='editar_solicitacao_jardinagem'
    ),

    path(
        'rejeitar-solicitacao-jardinagem/<str:userid>/<str:id_random>/',
        reject_solicitacao_jardinagem,
        name='reject_solicitacao_jardinagem'
    ),

    path(
        'aceitar-solicitacao-jardinagem/<str:userid>/<str:id_random>/',
        accept_solicitacao_jardinagem,
        name='accept_solicitacao_jardinagem'
    ),
    path(
        'confirmar-solicitacao-jardinagem/<str:type>/<str:userid>/<str:id_random>/',
        confirm_solicitacao_jardinagem,
        name='confirm_solicitacao_jardinagem'
    ),
    path(
        'exportar-qr-code-jardinagem.png/<str:id_random>/',
        exportar_qr_code_jardinagem_png,
        name='exportar_qr_code_jardinagem_png'
    ),
    path(
        'exportar-qr-code-jardinagem.pdf/<str:id_random>/',
        exportar_qr_code_jardinagem_pdf,
        name='exportar_qr_code_jardinagem_pdf'
    ),

    path('delete-QRCODE-jardinagem/<str:userid>/<str:id_random>/', IfDeleteQRCodeJardinagem, name='IfDeleteQRCodeJardinagem'),
    path('DeleteQRCodeJardinagem/<str:id_random>/', DeleteQRCodeJardinagem, name="DeleteQRCodeJardinagem"),

]