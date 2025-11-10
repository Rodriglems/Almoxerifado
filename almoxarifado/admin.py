from django.contrib import admin
from .models import Produto, CategoriaProduto, SaidaProduto, Instituicao, Funcionario

# Register your models here.
admin.site.register(Instituicao)
admin.site.register(Funcionario)
admin.site.register(CategoriaProduto)
admin.site.register(Produto)
admin.site.register(SaidaProduto)
