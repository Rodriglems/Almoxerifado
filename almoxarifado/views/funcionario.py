from ..models import Funcionario
from django.shortcuts import render, redirect

def lista_funcionario(request):
    funcionario = Funcionario.objects.all()
    return render(request, 'funcionario/lista.html', {'funcionario': funcionario})

def add_funcionario(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        data_nascimento = request.POST.get('dat_nascimento')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        instituicao = request.POST.get('instituicao')
        
        Funcionario.objects.create(
            name=name,
            data_nascimento=data_nascimento,
            email=email,
            telefone=telefone,
            instituicao=instituicao
        )
        return redirect('lista_funcionario')
    return render(request, 'funcionario/Addfuncionario.html')