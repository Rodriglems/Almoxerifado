from ..models import Instituicao
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
import logging
from django.db import IntegrityError


def lista_instituicao(request):
    instituicoes = Instituicao.objects.all()
    return render(request, 'instituicao/lista.html', {'instituicoes': instituicoes})


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
    # se estiver pedindo download em PDF, tente usar xhtml2pdf; caso contrário renderiza o HTML
    if request.GET.get('download') == 'pdf':
        try:
            from xhtml2pdf import pisa
            html = render_to_string('instituicao/pdf.html', {'instituicoes': instituicoes})
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="instituicoes.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                logging.exception('Erro ao gerar PDF com xhtml2pdf')
                return HttpResponse('Erro ao gerar PDF', status=500)
            return response
        except Exception as e:
            logging.exception('Não foi possível gerar PDF, retornando HTML')
            return render(request, 'instituicao/pdf.html', {'instituicoes': instituicoes, 'warning': str(e)})

    return render(request, 'instituicao/pdf.html', {'instituicoes': instituicoes})


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
        nome = request.POST.get('nome', '').strip()
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
