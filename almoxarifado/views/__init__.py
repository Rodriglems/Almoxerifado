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
]
