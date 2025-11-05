from almoxarifado.models import Funcionario, Instituicao
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm



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
    return render(request, 'funcionario/inicio.html')

@login_required
def editar_funcionario(request, pk):
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
        # outros validados rápidos...

        if erros:
            return render(request, 'funcionario/Addfuncionario.html', {'erros': erros, 'val': request.POST, 'instituicoes': Instituicao.objects.all()})

        try:
            with transaction.atomic():
                # tenta achar/usar usuário pelo email (ou criar)
                user, created = User.objects.get_or_create(username=email, defaults={'email': email})
                # evita associar user que já tem funcionário
                from almoxarifado.models import Funcionario
                if hasattr(user, 'funcionario') and not created:
                    erros['email'] = 'Já existe um funcionário associado a este usuário/email.'
                    return render(request, 'funcionario/Addfuncionario.html', {'erros': erros, 'val': request.POST, 'instituicoes': Instituicao.objects.all()})

                # cria Funcionario apontando para user
                instituicao = None
                if instituicao_id:
                    from almoxarifado.models import Instituicao
                    instituicao = Instituicao.objects.filter(pk=instituicao_id).first()
            # cria Funcionario apontando para user
                instituicao = None
                if instituicao_id:
                    from almoxarifado.models import Instituicao
                    instituicao = Instituicao.objects.filter(pk=instituicao_id).first()

                funcionario = Funcionario.objects.create(
                    user=user,
                    nome=nome,
                    data_nascimento=data_nascimento or None,
                    email=email,
                    telefone=telefone,
                    instituicao=instituicao
                )
                # se quiser, marque senha inválida (sem login) até criar fluxo de senha
                user.set_unusable_password()
                user.save()

            return redirect('lista_funcionario')
        except IntegrityError as e:
            erros['__all__'] = 'Erro ao cadastrar funcionário: dado duplicado.'
            return render(request, 'funcionario/Addfuncionario.html', {'erros': erros, 'val': request.POST, 'instituicoes': Instituicao.objects.all()})
        except Exception as e:
            return render(request, 'funcionario/Addfuncionario.html', {'error': str(e), 'val': request.POST, 'instituicoes': Instituicao.objects.all()})

    return render(request, 'funcionario/Addfuncionario.html', {'instituicoes': Instituicao.objects.all()})

@login_required
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('lista_funcionario')
    return render(request, 'funcionario/confirmar_exclusao.html', {'funcionario': funcionario})

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
