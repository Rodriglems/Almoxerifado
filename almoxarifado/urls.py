from django.urls import path 
from .views import funcionario

urlpatterns = [
    path ('', funcionario.lista_funcionario, name = 'lista_funcionario'),
    path ('addfuncionario', funcionario.add_funcionario, name= 'add_funcionario'),
    ]