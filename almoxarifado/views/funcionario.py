from almoxarifado.models import Funcionario, Instituicao
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages


@login_required
def lista_funcionario(request):
    q = request.GET.get('q', '').strip()
    # ordenar por nome para garantir resultados consistentes ao paginar
    funcionarios = Funcionario.objects.all().order_by('nome')
    if q:
        funcionarios = funcionarios.filter(Q(nome__icontains=q)).order_by('nome')

    paginator = Paginator(funcionarios, 10)  # 10 funcionários por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'funcionario/lista.html', {'funcionarios': page_obj, 'page_obj': page_obj})
     

@login_required
def add_funcionario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        instituicao_id = request.POST.get('instituicao')
        senha = request.POST.get('senha')

        try:
            with transaction.atomic():
                instituicao = get_object_or_404(Instituicao, id=instituicao_id)
                user = User.objects.create_user(username=email, email=email, password=senha)
                

                Funcionario.objects.create(
                    nome=nome,
                    data_nascimento=data_nascimento,
                    email=email,
                    telefone=telefone,
                    instituicao=instituicao,
                    user=user  # atribui o usuário logado
                )
            return redirect('lista_funcionario')
        except Exception as e:
            instituicoes = Instituicao.objects.all()
            return render(request, 'funcionario/Addfuncionario.html', {
                'instituicoes': instituicoes,
                'error': f'Erro ao cadastrar funcionário: {str(e)}'
            })

    instituicoes = Instituicao.objects.all()
    return render(request, 'funcionario/Addfuncionario.html', {'instituicoes': instituicoes})

@login_required
def inicio_projeto(request):
    return render(request, 'inicio.html')

@login_required
def editar_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        data_nascimento = request.POST.get('data_nascimento', '').strip()
        email = request.POST.get('email', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        instituicao_id = request.POST.get('instituicao')

        erros = {}
        if not nome:
            erros['nome'] = 'Nome obrigatório.'
        if not email:
            erros['email'] = 'Email obrigatório.'

        if erros:
            return render(request, 'funcionario/Addfuncionario.html', {
                'erros': erros, 
                'val': request.POST, 
                'instituicoes': Instituicao.objects.all(),
                'funcionario': funcionario
            })

        try:
            with transaction.atomic():
                # Atualiza campos do funcionário existente
                funcionario.nome = nome
                funcionario.data_nascimento = data_nascimento or None
                funcionario.email = email
                funcionario.telefone = telefone
                
                if instituicao_id:
                    funcionario.instituicao = get_object_or_404(Instituicao, pk=instituicao_id)
                else:
                    funcionario.instituicao = None
                
                # Atualiza o usuário associado se existir
                if funcionario.user:
                    funcionario.user.username = email
                    funcionario.user.email = email
                    funcionario.user.save()
                
                funcionario.save()
                
            messages.success(request, 'Funcionário editado com sucesso!')    
            return redirect('lista_funcionario')
        except IntegrityError as e:
            erros['__all__'] = 'Erro ao editar funcionário: dado duplicado.'
            return render(request, 'funcionario/Addfuncionario.html', {
                'erros': erros, 
                'val': request.POST, 
                'instituicoes': Instituicao.objects.all(),
                'funcionario': funcionario
            })
        except Exception as e:
            return render(request, 'funcionario/Addfuncionario.html', {
                'error': str(e), 
                'val': request.POST, 
                'instituicoes': Instituicao.objects.all(),
                'funcionario': funcionario
            })

    # GET: preenche formulário com dados atuais
    val = {
        'nome': funcionario.nome,
        'data_nascimento': funcionario.data_nascimento,
        'email': funcionario.email,
        'telefone': funcionario.telefone,
        'instituicao': funcionario.instituicao.pk if funcionario.instituicao else ''
    }
    return render(request, 'funcionario/Addfuncionario.html', {
        'instituicoes': Instituicao.objects.all(),
        'funcionario': funcionario,
        'val': val
    })

@login_required
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    if request.method == 'POST':
        nome_funcionario = funcionario.nome  # Salva o nome antes de excluir
        funcionario.delete()
        messages.success(request, f'Funcionário "{nome_funcionario}" excluído com sucesso!')
        return redirect('lista_funcionario')
    
    # GET: mostra página de confirmação
    return render(request, 'funcionario/lista.html', {'funcionario': funcionario})

@login_required
def pdf_funcionario(request):
    funcionarios = Funcionario.objects.all()
    template_path = 'funcionario/pdf.html'
    context = {'funcionarios': funcionarios}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="funcionarios.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)
    return response
