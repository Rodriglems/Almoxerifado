from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from almoxarifado.models import CategoriaProduto, Produto
from django.contrib import messages

def listar_categorias(request):
    q = request.GET.get('q', '').strip()
    categorias = CategoriaProduto.objects.all()
    if q:
        categorias = categorias.filter(Q(nome__icontains=q) | Q(descricao__icontains=q))

    paginator = Paginator(categorias, 10)  # 10 categorias por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categoria/lista.html', {'categorias': page_obj, 'page_obj': page_obj})  


def add_categoria(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')   
        CategoriaProduto.objects.create(nome=nome)
        # se o name da sua rota de listar for 'lista_categoria', troque abaixo conforme seu urls.py
        return redirect('listar_categorias')
    # GET -> renderiza o formulário de adicionar
    return render(request, 'categoria/adcionar.html')  # novo template só com o form


def categoria_produto(request, categoria_id):
     # Busca a categoria específica ou retorna 404 se não existir
     categoria = get_object_or_404(CategoriaProduto, id=categoria_id)
     
     # Filtra apenas os produtos desta categoria
     q = request.GET.get('q', '').strip()
     produtos = Produto.objects.filter(categoria=categoria)
     
     if q:
        produtos = produtos.filter(Q(nome__icontains=q) | Q(descricao__icontains=q))

     paginator = Paginator(produtos, 10)  # 10 produtos por página
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
     
     return render(request, 'categoria/categoria_produto.html', {
         'produtos': page_obj, 
         'page_obj': page_obj,
         'categoria': categoria
     })
     

def excluir_categoria(request, pk):
    categoria = get_object_or_404(CategoriaProduto, pk=pk)
    nome_categoria = categoria.nome 
    categoria.delete()
    messages.success(request, f'Categoria "{nome_categoria}" excluída com sucesso!')
    return redirect('listar_categorias')

def editar_categoria(request, pk):
    categoria = get_object_or_404(CategoriaProduto, pk=pk)
    
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.save()
        messages.success(request, 'Categoria atualizada com sucesso!')
        return redirect('listar_categorias')
    
    # Se for GET, mostra o formulário de edição
    return render(request, 'categoria/editar.html', {'categoria': categoria})