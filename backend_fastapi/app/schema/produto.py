# app/schemas/produto.py
from pydantic import BaseModel, root_validator
from typing import Optional, List
from datetime import datetime
from app.models.produto import Produto


# Esquema básico para Produto
class ProdutoSchema(BaseModel):
    codigo: int  # Código do Produto
    nome_produto: str  # Nome do Produto
    und_servicos: str  # Unidade de Serviço (Ex: "Un", "Kg", "M²")

    # Relacionamentos (pode ser opcional ou pode ser adicionado conforme sua necessidade)
    usuario_id: Optional[int] = None  # ID do usuário que criou o produto
    componente_id: Optional[int] = None  # ID do componente associado
    operacao_id: Optional[int] = None  # ID da operação associada
    grupo_produto_id: Optional[int] = None  # ID do grupo de produto
    posto_trabalho_id: Optional[int] = None  # ID do posto de trabalho

    # Campos de controle
    created_at: Optional[datetime] = None  # Data de criação
    updated_at: Optional[datetime] = None  # Data de atualização
    deleted_at: Optional[datetime] = None  # Data de exclusão (se houver)

    @root_validator(pre=True)
    def convert_to_uppercase(cls, values):
        # Itera sobre os campos e converte os valores do tipo str para maiúsculas
        for field, value in values.items():
            if isinstance(value, str):  # Verifica se o valor é uma string
                values[field] = value.upper()  # Converte para maiúsculas
        return values

# Esquema de Produto para exibição pública (com relacionamentos)
class ProdutoPublic(ProdutoSchema):
    id: int  # ID do Produto

    # Relacionamentos, caso deseje exibir
    usuario_id: Optional[int]
    componente_id: Optional[int]
    operacao_id: Optional[int]
    grupo_produto_id: Optional[int]
    posto_trabalho_id: Optional[int]


# Exibição de múltiplos produtos (com paginação)
class ProdutoList(BaseModel):
    produtos: List[ProdutoPublic]  # Lista de Produtos
    offset: int  # Offset da paginação
    limit: int  # Limite da paginação


# Esquema para atualização de Produto
class ProdutoUpdate(BaseModel):
    codigo: Optional[int] = None  # Código do Produto
    nome_produto: Optional[str] = None  # Nome do Produto
    und_servicos: Optional[str] = None  # Unidade de Serviço (Ex: "Un", "Kg", "M²")

    # Relacionamentos (caso queira atualizar)
    usuario_id: Optional[int] = None  # ID do usuário que criou o produto
    componente_id: Optional[int] = None  # ID do componente associado
    operacao_id: Optional[int] = None  # ID da operação associada
    grupo_produto_id: Optional[int] = None  # ID do grupo de produto
    posto_trabalho_id: Optional[int] = None  # ID do posto de trabalho

    # Campos de controle
    updated_at: Optional[datetime] = None  # Data de atualização
    deleted_at: Optional[datetime] = None  # Data de exclusão (se houver)

    @root_validator(pre=True)
    def convert_to_uppercase(cls, values):
        # Itera sobre os campos e converte os valores do tipo str para maiúsculas
        for field, value in values.items():
            if isinstance(value, str):  # Verifica se o valor é uma string
                values[field] = value.upper()  # Converte para maiúsculas
        return values
