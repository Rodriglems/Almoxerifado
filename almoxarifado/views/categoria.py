from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from almoxarifado.models import CategoriaProduto, Produto
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required

@login_required
def listar_categorias(request):
    q = request.GET.get('q', '').strip()
    categorias = CategoriaProduto.objects.all()
    if q:
        categorias = categorias.filter(Q(nome__icontains=q) | Q(descricao__icontains=q))

    paginator = Paginator(categorias, 10)  # 10 categorias por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categoria/lista.html', {'categorias': page_obj, 'page_obj': page_obj})  

@login_required
def add_categoria(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')   
        CategoriaProduto.objects.create(nome=nome)
        # se o name da sua rota de listar for 'lista_categoria', troque abaixo conforme seu urls.py
        return redirect('listar_categorias')
    # GET -> renderiza o formulário de adicionar
    return render(request, 'categoria/adcionar.html')  # novo template só com o form

@login_required
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
     
@login_required
def excluir_categoria(request, pk):
    categoria = get_object_or_404(CategoriaProduto, pk=pk)
    nome_categoria = categoria.nome 
    categoria.delete()
    messages.success(request, f'Categoria "{nome_categoria}" excluída com sucesso!')
    return redirect('listar_categorias')
@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(CategoriaProduto, pk=pk)
    
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.save()
        messages.success(request, 'Categoria atualizada com sucesso!')
        return redirect('listar_categorias')
    
    # Se for GET, mostra o formulário de edição
    return render(request, 'categoria/editar.html', {'categoria': categoria})


@login_required
def pdf_categoria(request, categoria_id):
    import os
    import base64
    from django.conf import settings
    
    # Busca a categoria específica
    categoria = get_object_or_404(CategoriaProduto, id=categoria_id)
    
    # Filtra apenas os produtos desta categoria
    produtos = Produto.objects.filter(categoria=categoria)
    
    template_path = 'categoria/pdf.html'
    
    # Converter imagem para base64 (mesmo código do pdf_produtos)
    logo_base64 = None
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'image1.png')
    
    try:
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as image_file:
                logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
    
    context = {
        'produtos': produtos,
        'categoria': categoria,
        'logo_base64': logo_base64
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="produtos_{categoria.nome}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)
    return response
