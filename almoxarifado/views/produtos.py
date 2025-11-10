from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from almoxarifado.models import Produto, CategoriaProduto
from django.contrib import messages
from almoxarifado.models import SaidaProduto
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required


@login_required
def listar_produtos(request):
    q = request.GET.get('q', '').strip()
    produtos = Produto.objects.all()
    if q:
        produtos = produtos.filter(Q(nome__icontains=q))

    paginator = Paginator(produtos, 10)  # 10 produtos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'produtos/lista.html', {'produtos': page_obj, 'page_obj': page_obj})

@login_required
def add_produtos(request):
    if request.method == 'POST':
        nome = (request.POST.get('nome') or '').strip()
        descricao = (request.POST.get('descricao') or '').strip()
        categoria_id = request.POST.get('categoria')
        quantidade_estoque_raw = request.POST.get('quantidade_estoque', '0')

        errors = []

        if not nome:
            errors.append('O campo nome é obrigatório.')

        # Validar e converter quantidade_estoque para inteiro
        try:
            quantidade_estoque = int(quantidade_estoque_raw)
            if quantidade_estoque < 0:
                raise ValueError()
        except (ValueError, TypeError):
            errors.append('Quantidade inválida. Informe um número inteiro maior ou igual a zero.')
            quantidade_estoque = 0

        categoria = None
        if categoria_id:
            try:
                categoria = CategoriaProduto.objects.get(id=categoria_id)
            except CategoriaProduto.DoesNotExist:
                errors.append('Categoria selecionada não existe.')

        form_data = {
            'nome': nome,
            'descricao': descricao,
            'quantidade_estoque': quantidade_estoque_raw,
            'categoria_id': categoria_id,
        }

        if errors:
            for e in errors:
                messages.error(request, e)
            categorias = CategoriaProduto.objects.all()
            return render(request, 'produtos/adicionar.html', {'categorias': categorias, 'form_data': form_data})

        Produto.objects.create(
            nome=nome,
            descricao=descricao,
            categoria=categoria,
            quantidade_estoque=quantidade_estoque
        )
        messages.success(request, 'Produto adicionado com sucesso!')
        return redirect('listar_produtos')

    categorias = CategoriaProduto.objects.all()
    return render(request, 'produtos/adicionar.html', {'categorias': categorias, 'form_data': {}})


@login_required
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    nome_produto = produto.nome  # Salva o nome antes de excluir
    produto.delete()
    messages.success(request, f'Produto "{nome_produto}" excluído com sucesso!')
    return redirect('listar_produtos')

@login_required
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


@login_required
def pdf_produtos(request):
    produtos = Produto.objects.all()
    template_path = 'produtos/pdf.html'
    context = {'produtos': produtos}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="produtos.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)
    return response



# Saída de Produtos
@login_required
def listar_saidas(request):
    q = request.GET.get('q', '').strip()
    saidas = SaidaProduto.objects.all().order_by('-data_saida')
    if q:
        saidas = saidas.filter(Q(produto__nome__icontains=q))

    paginator = Paginator(saidas, 10)  # 10 saídas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'produtos/lista_saida.html', {'saidas': page_obj, 'page_obj': page_obj})


@login_required
def registrar_saida(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        quantidade = request.POST.get('quantidade')
        destino = request.POST.get('destino', '')
        observacao = request.POST.get('observacao', '')
        produto = get_object_or_404(Produto, pk=produto_id)
        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError()
            if quantidade > produto.quantidade_estoque:
                messages.error(request, f'Estoque insuficiente para o produto "{produto.nome}". Estoque atual é de {produto.quantidade_estoque}.')
                return redirect('saida_produto')
        except (ValueError, TypeError):
            messages.error(request, 'Quantidade inválida.')
            return redirect('saida_produto')
        saida = SaidaProduto(produto=produto, quantidade=quantidade, destino=destino, observacao=observacao, usuario=request.user if request.user.is_authenticated else None)
        try:
            saida.save()
            produto.quantidade_estoque -= quantidade  # Reduz a quantidade do estoque
            produto.save()  # Salva a atualização no banco de dados
            messages.success(request, f'Saída registrada: {quantidade} x {produto.nome}. Estoque atualizado: {produto.quantidade_estoque}.')
        except Exception as e:
            messages.error(request, f'Erro ao registrar saída: {e}')
        return redirect('listar_saidas')

    produtos = Produto.objects.all()
    return render(request, 'produtos/saida.html', {'produtos': produtos})
