from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_funcionario, name='lista_funcionario'),
    path('addfuncionario/', views.add_funcionario, name='add_funcionario'),
    path('instituicao/', views.lista_instituicao, name='lista_instituicao'),
    path('addinstituicao/', views.add_instituicao, name='add_instituicao'),
]
