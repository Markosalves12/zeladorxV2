from django.urls import path
from kanban.views_jardinagem import kanban_jardinagem

urlpatterns = [
    path('kanban_jardinagem/<str:userid>', kanban_jardinagem, name='kanban_jardinagem'),
    # path('tabeladedados', tabeladedados, name='tabeladedados')
]