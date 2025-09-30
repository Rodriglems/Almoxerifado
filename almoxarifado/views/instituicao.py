from ..models import Instituicao
from django.shortcuts import render, redirect

def lista_instituicao(request):
    instituicoes = Instituicao.objects.all()
    return render(request, 'instituicao/lista.html', {'instituicoes': instituicoes})

def add_instituicao(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cep = request.POST.get("cep")
        logradouro = request.POST.get("logradouro")
        numero = request.POST.get("numero")
        bairro = request.POST.get("bairro")
        cidade = request.POST.get("cidade")
        estado = request.POST.get("estado")
        telefone = request.POST.get("telefone")
        cnpj = request.POST.get("cnpj")

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
        return redirect('lista_instituicao')
    return render(request, 'instituicao/Addinstituicao.html')
