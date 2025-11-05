from django.urls import path
from . import views

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
    
    
# Categoria URLs
    path('categoria/', views.listar_categorias, name='listar_categorias'),
    path('adcionar/categoria/', views.add_categoria, name='add_categoria'),
    path('categoria/<int:categoria_id>/produtos/', views.categoria_produto, name='categoria_produto'),
    path('excluir-categoria/<int:pk>/', views.excluir_categoria, name='excluir-categoria'),
    path('editar-categoria/<int:pk>/', views.editar_categoria, name='editar-categoria'),
    path('pdf-categoria/<int:categoria_id>/', views.pdf_categoria, name='pdf_categoria'),
    
    
# Produtos
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('adicionar/produto/', views.add_produtos, name='add_produto'),
    path('excluir-produtos/<int:pk>/', views.excluir_produto, name="excluir-produto"),
    path('editar-produto/<int:pk>/', views.editar_produto, name="editar-produto"),
    path('pdf-produtos/', views.pdf_produtos, name='pdf_produtos'),
    

]
