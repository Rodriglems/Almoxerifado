from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Instituicao(models.Model):
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    telefone = models.CharField(max_length=20)
    cnpj = models.CharField(max_length=18, unique=True)
    
    def __str__(self):
        return self.nome
    
class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)

    def __str__(self):
         return self.nome
     
     
class CategoriaProduto(models.Model):
    produtos = models.ManyToManyField('Produto', related_name='categorias', blank=True)
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    quantidade_estoque = models.PositiveIntegerField(default=0)
    entrada_estoque = models.DateField(auto_now_add=True)
    saida_estoque = models.DateField(null=True, blank=True)
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome


class SaidaProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='saidas')
    quantidade = models.PositiveIntegerField()
    data_saida = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    destino = models.CharField(max_length=200, blank=True)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome} em {self.data_saida.strftime("%Y-%m-%d %H:%M")}'