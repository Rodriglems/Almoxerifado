from almoxarifado.models import Instituicao
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
import logging
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from xhtml2pdf import pisa  
from django.template.loader import get_template


@login_required
def lista_instituicao(request):
 
    q = request.GET.get('q', '').strip()
    instituicoes = Instituicao.objects.all()
    if q:
        instituicoes = instituicoes.filter(Q(nome__icontains=q))

    paginator = Paginator(instituicoes, 10)  # 10 instituições por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'instituicao/lista.html', {'instituicoes': page_obj, 'page_obj': page_obj})
     
@login_required
def add_instituicao(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        cep = request.POST.get("cep", "").strip()
        logradouro = request.POST.get("logradouro", "").strip()
        numero = request.POST.get("numero", "").strip()
        bairro = request.POST.get("bairro", "").strip()
        cidade = request.POST.get("cidade", "").strip()
        estado = request.POST.get("estado", "").strip()
        telefone = request.POST.get("telefone", "").strip()
        cnpj = request.POST.get("cnpj", "").strip()

        erros = {}
        if not nome:
            erros['nome'] = 'Nome é obrigatório.'
        if not cnpj:
            erros['cnpj'] = 'CNPJ é obrigatório.'

        if erros:
            return render(request, 'instituicao/Addinstituicao.html', {'erros': erros, 'val': request.POST})

        try:
            nova_instituicao = Instituicao(
                nome=nome,
                cep=cep,
                logradouro=logradouro,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                telefone=telefone,
                cnpj=cnpj
            )
            nova_instituicao.save()
        except IntegrityError:
            erros['cnpj'] = 'Já existe uma instituição com esse CNPJ.'
            return render(request, 'instituicao/Addinstituicao.html', {'erros': erros, 'val': request.POST})
        except Exception as e:
            logging.exception('Erro ao salvar instituição')
            return render(request, 'instituicao/Addinstituicao.html', {'error': str(e), 'val': request.POST})

        return redirect('lista_instituicao')
    return render(request, 'instituicao/Addinstituicao.html')

def pdf_instituicao(request):
    instituicoes = Instituicao.objects.all()
    template_path = 'instituicao/pdf.html'
    context = {'instituicoes': instituicoes}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="instituicoes.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)
    return response


def excluir_instituicao(request, pk):
    instituicao = get_object_or_404(Instituicao, pk=pk)
    if request.method == 'POST':
        instituicao.delete()
        return redirect('lista_instituicao')
    # se GET, renderiza uma confirmação simples
    return render(request, 'instituicao/confirm_delete.html', {'instituicao': instituicao})


def editar_instituicao(request, pk):
    instituicao = get_object_or_404(Instituicao, pk=pk)
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip() #remove os espaço atrás e na frente
        cep = request.POST.get('cep', '').strip()
        logradouro = request.POST.get('logradouro', '').strip()
        numero = request.POST.get('numero', '').strip()
        bairro = request.POST.get('bairro', '').strip()
        cidade = request.POST.get('cidade', '').strip()
        estado = request.POST.get('estado', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        cnpj = request.POST.get('cnpj', '').strip()

        erros = {}
        if not nome:
            erros['nome'] = 'Nome é obrigatório.'
        if not cnpj:
            erros['cnpj'] = 'CNPJ é obrigatório.'

        if erros:
            return render(request, 'instituicao/editinstituicao.html', {'erros': erros, 'val': request.POST, 'instituicao': instituicao})

        # atualização
        instituicao.nome = nome
        instituicao.cep = cep
        instituicao.logradouro = logradouro
        instituicao.numero = numero
        instituicao.bairro = bairro
        instituicao.cidade = cidade
        instituicao.estado = estado
        instituicao.telefone = telefone
        instituicao.cnpj = cnpj
        try:
            instituicao.save()
        except IntegrityError:
            erros['cnpj'] = 'Já existe outra instituição com esse CNPJ.'
            return render(request, 'instituicao/editinstituicao.html', {'erros': erros, 'val': request.POST, 'instituicao': instituicao})

        return redirect('lista_instituicao')

    # GET -> renderiza formulário pré-preenchido
    return render(request, 'instituicao/editinstituicao.html', {'instituicao': instituicao})
