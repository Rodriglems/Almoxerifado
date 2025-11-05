# Importando todas as views dos módulos para disponibilizar no pacote views
from .funcionario import (
    lista_funcionario,
    add_funcionario,
    inicio_projeto,
    editar_funcionario,
    excluir_funcionario,
    pdf_funcionario,
    
)

__all__ = [
    'lista_funcionario',
    'add_funcionario',
    'inicio_projeto',
    'editar_funcionario',
    'excluir_funcionario',
    'pdf_funcionario',
    'cadastrar_usuario',
    'login_view',
    'logout_view',
    
]

from .instituicao import (
    lista_instituicao,
    add_instituicao,
    editar_instituicao,
    excluir_instituicao,
    pdf_instituicao,
)
from ..login import login_view, logout_view

# Expose all public view names from the package
__all__ = [
    # funcionario
    'lista_funcionario',
    'add_funcionario',
    'inicio_projeto',
    'editar_funcionario',
    'excluir_funcionario',
    'pdf_funcionario',
    'login_view',
    'logout_view',
    # instituicao
    'lista_instituicao',
    'add_instituicao',
    'editar_instituicao',
    'excluir_instituicao',
    'pdf_instituicao',
    #categoria
    'listar_categorias',
    'add_categoria',
    'categoria_produto',
    'excluir_categoria',
    'editar_categoria',
    #produtos
    'listar_produtos',
    'add_produtos',
    'excluir_produto',
    'editar_produto',
    
]

# Expor funções de view definidas em submódulos para compatibilidade com imports
# (ex.: from almoxarifado import views; views.listar_categorias)
from .categoria import listar_categorias, add_categoria, categoria_produto, excluir_categoria, editar_categoria

# Se tiver outras views em submódulos que o urls.py referencia via almoxarifado.views,
# adicione-as aqui também, por exemplo:
# from .instituicao import pdf_instituicao, add_instituicao
# from .funcionario import lista_funcionario

from .produtos import listar_produtos, add_produtos, excluir_produto, editar_produto
