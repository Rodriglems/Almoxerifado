from ..models import Funcionario, Instituicao
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from xhtml2pdf import pisa


def lista_funcionario(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'funcionario/lista.html', {'funcionarios': funcionarios})

def add_funcionario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        instituicao_id = request.POST.get('instituicao')
        
        try:
            instituicao = get_object_or_404(Instituicao, id=instituicao_id)
            Funcionario.objects.create(
                nome=nome,
                data_nascimento=data_nascimento,
                email=email,
                telefone=telefone,
                instituicao=instituicao
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

def inicio_projeto(request):
    """Renderiza o template de boas-vindas localizado em 'funcionario/inicio.html'."""
    return render(request, 'funcionario/inicio.html')

def pdf_instituicao(request):
    instituicoes = Instituicao.objects.all()
    template_path = 'instituicao/pdf.html'
    context = {'instituiçoes': instituicoes}
    html = render(request, template_path, context).content.decode('utf-8')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="instituicoes.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Erro ao gerar PDF", status=500)
    return response
    