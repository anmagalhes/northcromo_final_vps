# app/api/models/__init__.py
#python create_tables.py

#uvicorn app.main:app --reload

#LINK DO ARQUVO
#https://docs.google.com/spreadsheets/d/15Jyo4qMmVK0JTSB95__JaVJveAOflbS1qR0qNOucEgI/edit?gid=1452100669#gid=1452100669

#.\venv\Scripts\Activate.ps1


from app.api.models.base import Base  # Base declarativa

# Importar modelos
from app.api.models.cliente import Cliente
from app.api.models.usuario import Usuario
from app.api.models.recebimento import Recebimento
from app.api.models.checklist_recebimento import ChecklistRecebimento
from app.api.models.componente import Componente
from app.api.models.operacao import Operacao
from app.api.models.posto_trabalho import Posto_Trabalho
from app.api.models.defeito import Defeito
from app.api.models.produto_tarefa  import Produto_Tarefa

from app.api.models.cliente import Cliente
from app.api.models.fornecedor import Fornecedor
from app.api.models.produto_fornecedor import ProdutoFornecedor
from app.api.models.produto import Produto
from app.api.models.funcionario import Funcionario
from app.api.models.funcao import Funcao
from app.api.models.notafiscal import NotaFiscal





# python create_tables.py
__all__ = [
    "Base",
    "Cliente",
    "Usuario",
    "Recebimento",
    "ChecklistRecebimento",
    "Componente",
    "Operacao",
    "Produto_Tarefa",
    "Posto_Trabalho",
    "Defeito",
    "Cliente",
    "Fornecedor",
    "Produto",
    "ProdutoFornecedor",
    "Funcionario",
    "Funcao",
    "NotaFiscal"
]
