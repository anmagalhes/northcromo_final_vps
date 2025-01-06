# app/schemas/itens_recebimento.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from app.schema.produto import ProdutoPublic
from app.schema.funcionario import FuncionarioPublic
from app.schema.recebimento.recebimento import RecebimentoPublic


# Enum de Status da Ordem
class StatusOrdemEnum(Enum):
    PENDENTE = 1
    FINALIZADO = 5
    CANCELADO = 3
    EM_ANDAMENTO = 2


# Esquema básico para item de recebimento
class ItensRecebimentoSchema(BaseModel):
    qtd_produto: int  # Quantidade de produtos no item de recebimento
    preco_unitario: float  # Preço unitário
    preco_total: float  # Preço total (qtd_produto * preco_unitario)
    referencia_produto: Optional[str] = None  # Referência do produto
    status_ordem: StatusOrdemEnum  # Status do item de recebimento

    produto_id: int  # ID do produto relacionado
    recebimento_id: int  # ID do recebimento relacionado
    funcionario_id: Optional[int] = None  # ID do funcionário relacionado (se houver)

    class Config:
        orm_mode = True


# Inclusão do ID após a criação do item de recebimento
class ItensRecebimentoPublic(ItensRecebimentoSchema):
    id: int
    produto: Optional[ProdutoPublic]  # Produto completo (relacionado)
    funcionario: Optional[FuncionarioPublic]  # Funcionario completo (opcional)
    recebimento: RecebimentoPublic  # Recebimento completo (relacionado)


# Exibição para usuário final
class ItensRecebimentoList(BaseModel):
    itensRecebimento: list[ItensRecebimentoPublic]
    offset: int
    limit: int


# Criar Novo Item de Recebimento
class ItensRecebimentoCreate(BaseModel):
    qtd_produto: int
    preco_unitario: float
    preco_total: float
    referencia_produto: Optional[str] = None
    status_ordem: StatusOrdemEnum  # Status da ordem (como 'PENDENTE', 'FINALIZADO', etc.)

    produto_id: int  # ID do produto
    recebimento_id: int  # ID do recebimento
    funcionario_id: Optional[int] = None  # ID do funcionário (se houver)

    class Config:
        orm_mode = True


# Atualizar Item de Recebimento
class ItensRecebimentoUpdate(BaseModel):
    qtd_produto: Optional[int] = None
    preco_unitario: Optional[float] = None
    preco_total: Optional[float] = None
    referencia_produto: Optional[str] = None
    status_ordem: Optional[StatusOrdemEnum] = None

    class Config:
        orm_mode = True
