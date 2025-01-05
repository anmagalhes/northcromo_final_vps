# app/schemas/itens_recebimento.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

# Importando schemas relacionados a produtos, recebimentos e funcionários
from app.schema.produto import ProdutoPublic
from app.schema.funcionario import FuncionarioPublic
from app.schema.recebimento.recebimento  import RecebimentoPublic

# Definindo o Enum de StatusOrdem para o esquema
class StatusOrdemEnum(Enum):
    PENDENTE = 1
    FINALIZADO = 5
    CANCELADO = 3
    EM_ANDAMENTO = 2


# Esquema básico para um item de recebimento
class ItensRecebimentoSchema(BaseModel):
    qtd_produto: int  # Quantidade de produtos no item de recebimento
    preco_unitario: float  # Preço unitário
    preco_total: float  # Preço total (qtd_produto * preco_unitario)
    referencia_produto: Optional[str] = None  # Referência do produto
    status_ordem: StatusOrdemEnum  # Status do item de recebimento

    produto_id: int  # ID do produto relacionado
    recebimento_id: int  # ID do recebimento relacionado
    funcionario_id: Optional[int] = None  # ID do funcionário relacionado (se houver)

# Inclusão do ID depois de criação
class ItensRecebimentoPublic(ItensRecebimentoSchema):
    id: int
    produto: Optional[ProdutoPublic]  # Produto completo (relacionado)
    funcionario: Optional[FuncionarioPublic]  # Funcionario completo (opcional)
    recebimento: RecebimentoPublic  # Recebimento completo (relacionado)

# Exibisão publicar para usuario final
class ItensRecebimentoList(BaseModel):
    itensRecebimento: list[ItensRecebimentoPublic]
    offset: int
    limit: int


#Alterar somente os campos necessários
class ItensRecebimentoUpdate(BaseModel):
    name: str | None = None

#CRIAR
class ItensRecebimentoCreate(BaseModel):
    qtd_produto: int
    preco_unitario: float
    preco_total: float
    referencia_produto: Optional[str] = None
    status_ordem: str  # Um status de ordem, como 'PENDENTE', 'FINALIZADO', etc.

    produto_id: int  # ID do produto relacionado
    recebimento_id: int  # ID do recebimento relacionado
    funcionario_id: Optional[int] = None  # ID do funcionário relacionado (se houver)

    class Config:
        orm_mode = True

# ATUALIZAR
class ItensRecebimentoUpdate(BaseModel):
    qtd_produto: Optional[int] = None
    preco_unitario: Optional[float] = None
    preco_total: Optional[float] = None
    referencia_produto: Optional[str] = None
    status_ordem: Optional[str] = None

    class Config:
        orm_mode = True
