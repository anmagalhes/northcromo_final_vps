# app/schemas/produto.py
from pydantic import BaseModel
from typing import Optional, List

from app.models.produto import Produto

# Esquema para exibir um produto básico
class ProdutoSchema(BaseModel):
    codigo_produto: str  # Código do produto
    nome_produto: str  # Nome do produto
    descricao_produto: Optional[str] = None  # Descrição (opcional)
    referencia_produto: Optional[str] = None  # Referência do produto (opcional)
    qtd_produto: int  # Quantidade do produto


# Esquema para exibição pública (com id)
class ProdutoPublic(ProdutoSchema):
    id: int  # ID do produto no banco de dados


# Esquema para retornar uma lista de produtos
class ProdutoList(BaseModel):
    produtos: List[ProdutoPublic]  # Lista de produtos com detalhes completos
    offset: int  # Para paginação
    limit: int  # Para paginação

# Esquema para atualizar um produto
class ProdutoUpdate(BaseModel):
    nome_produto: Optional[str] = None  # Nome do produto (opcional para atualização)
    descricao_produto: Optional[str] = None  # Descrição do produto (opcional)
    referencia_produto: Optional[str] = None  # Referência do produto (opcional)
    qtd_produto: Optional[int] = None  # Quantidade do produto (opcional)




