from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from almoxarifado.models import Produto, CategoriaProduto
from django.contrib import messages



def listar_produtos(request):
    q = request.GET.get('q', '').strip()
    produtos = Produto.objects.all()
    if q:
        produtos = produtos.filter(Q(nome__icontains=q))

    paginator = Paginator(produtos, 10)  # 10 produtos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'produtos/lista.html', {'produtos': page_obj, 'page_obj': page_obj})

def add_produtos(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        categoria_id = request.POST.get('categoria')
        quantidade_estoque = request.POST.get('quantidade_estoque', '0')

        # Validar e converter quantidade_estoque para inteiro
        try:
            quantidade_estoque = int(quantidade_estoque)
        except (ValueError, TypeError):
            quantidade_estoque = 0

        categoria = None
        if categoria_id:
            try:
                categoria = CategoriaProduto.objects.get(id=categoria_id)
            except CategoriaProduto.DoesNotExist:
                pass
        
        Produto.objects.create(
            nome=nome, 
            descricao=descricao,
            categoria=categoria,
            quantidade_estoque=quantidade_estoque
        )
        messages.success(request, 'Produto adicionado com sucesso!')
        return redirect('listar_produtos')
    categorias = CategoriaProduto.objects.all()
    return render(request, 'produtos/adicionar.html', {'categorias': categorias})



def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    nome_produto = produto.nome  # Salva o nome antes de excluir
    produto.delete()
    messages.success(request, f'Produto "{nome_produto}" excluído com sucesso!')
    return redirect('listar_produtos')


def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        categoria_id = request.POST.get('categoria')
        quantidade_estoque = request.POST.get('quantidade_estoque', '0')

        # Validar e converter quantidade_estoque para inteiro
        try:
            produto.quantidade_estoque = int(quantidade_estoque)
        except (ValueError, TypeError):
            produto.quantidade_estoque = 0

        if categoria_id:
            try:
                produto.categoria = CategoriaProduto.objects.get(id=categoria_id)
            except CategoriaProduto.DoesNotExist:
                produto.categoria = None
        else:
            produto.categoria = None

        produto.save()
        messages.success(request, 'Produto atualizado com sucesso!')
        return redirect('listar_produtos')
    
    categorias = CategoriaProduto.objects.all()
    return render(request, 'produtos/editar.html', {'produto': produto, 'categorias': categorias})