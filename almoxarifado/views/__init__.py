# Importando todas as views dos módulos para disponibilizar no pacote views
from .funcionario import lista_funcionario, add_funcionario, inicio_projeto
from .instituicao import (
    lista_instituicao,
    add_instituicao,
    editar_instituicao,
    excluir_instituicao,
    pdf_instituicao,
)

__all__ = [
    'lista_funcionario',
    'add_funcionario',
    'inicio_projeto',
    'lista_instituicao',
    'add_instituicao',
    'editar_instituicao',
    'excluir_instituicao',
    'pdf_instituicao',
]

