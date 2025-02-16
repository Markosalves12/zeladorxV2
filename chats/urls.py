from django.urls import path
from chats.views import chats_jardinagem, get_mensagens, enviar_mensagem, carregar_mensagens

urlpatterns = [
    path('chats_jardinagem/<str:id_random>', chats_jardinagem, name='chats_jardinagem'),
    path('mensagens/<int:chat_id>/', get_mensagens, name='get_mensagens'),
    path('enviar_mensagem/<int:chat_id>/<str:id_random>/', enviar_mensagem, name='enviar_mensagem'),
    path('carregar_mensagens/<str:chat_id>/', carregar_mensagens, name='carregar_mensagens'),
]