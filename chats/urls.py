from django.urls import path
from chats.views import chats

urlpatterns = [
    path('chats', chats, name='chats'),
    # path('tabeladedados', tabeladedados, name='tabeladedados')
]