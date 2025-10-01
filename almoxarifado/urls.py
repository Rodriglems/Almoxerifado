from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    
# Funcionário URLs
    path('', views.lista_funcionario, name='lista_funcionario'),
    path('addfuncionario/', views.add_funcionario, name='add_funcionario'),
    path('editarfuncionario/<int:pk>/', views.editar_funcionario, name='editar_funcionario'),
    path('excluirfuncionario/<int:pk>/', views.excluir_funcionario, name='excluir_funcionario'),   
    path('pdf-funcionario/', views.pdf_funcionario, name='pdf-funcionario'),


# Instituição URLs
    path('instituicao/', views.lista_instituicao, name='lista_instituicao'),
    path('addinstituicao/', views.add_instituicao, name='add_instituicao'),
    path('inicio/', views.inicio_projeto, name='inicio'),
    path('pdf_instituicao/', views.pdf_instituicao, name='pdf_instituicao'),
    path('excluir-instituicao/<int:pk>/', views.excluir_instituicao, name='excluir-instituicao'),
    path('editar-instituicao/<int:pk>/', views.editar_instituicao, name='editar-instituicao'),

# tela de login
     path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
