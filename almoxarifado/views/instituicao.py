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
from datetime import datetime
from django.conf import settings
import os


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

@login_required
def pdf_instituicao(request):
    instituicoes = Instituicao.objects.all()
    template_path = 'instituicao/pdf.html'
    
    # Adiciona a data atual formatada
    data_atual = datetime.now().strftime('%d/%m/%Y às %H:%M')
    
    context = {
        'instituicoes': instituicoes,
        'data_atual': data_atual,
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="instituicoes.pdf"' # o attachment; para download
    template = get_template(template_path)
    html = template.render(context) # converte o template para uma string HTML
    
    # Função para resolver o caminho dos arquivos estáticos
    def link_callback(uri, rel):
        """
        Converte URIs HTML para caminhos absolutos do sistema
        """
        # Remove a barra inicial se existir
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            # Remove o STATIC_URL e junta com o caminho da pasta static
            relative_path = uri.replace(sUrl, "")
            if sRoot and os.path.exists(sRoot):
                path = os.path.join(sRoot, relative_path)
            else:
                # Usa BASE_DIR/static quando STATIC_ROOT não existe
                path = os.path.join(settings.BASE_DIR, 'static', relative_path)
        else:
            return uri

        # Verifica se o arquivo existe antes de retornar
        if not os.path.isfile(path):
            # Tenta buscar no diretório static do projeto como fallback
            fallback_path = os.path.join(settings.BASE_DIR, 'static', uri.lstrip('/').replace(sUrl.lstrip('/'), ''))
            if os.path.isfile(fallback_path):
                return fallback_path
            raise Exception(f'Arquivo não encontrado: {path} (URI original: {uri})')
        
        return path
    
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)
    return response

@login_required
def excluir_instituicao(request, pk):
    instituicao = get_object_or_404(Instituicao, pk=pk)
    if request.method == 'POST':
        instituicao.delete()
        return redirect('lista_instituicao')
    # se GET, renderiza uma confirmação simples
    return render(request, 'instituicao/confirm_delete.html', {'instituicao': instituicao})

@login_required
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
