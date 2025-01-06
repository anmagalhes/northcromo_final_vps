# app/schemas/recebimento/itens_recebimento.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum

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


# Inclusão do ID após a criação do item de recebimento
class ItensRecebimentoPublic(ItensRecebimentoSchema):
    id: int

# Exibição para usuário final
class ItensRecebimentoList(BaseModel):
    itensRecebimento: list[ItensRecebimentoPublic]
    offset: int
    limit: int


# Atualizar Item de Recebimento
class ItensRecebimentoUpdate(BaseModel):
    qtd_produto: Optional[int] = None
    preco_unitario: Optional[float] = None
    preco_total: Optional[float] = None
    referencia_produto: Optional[str] = None
    status_ordem: Optional[StatusOrdemEnum] = None

# Chame o update_forward_refs após a definição dos modelos
ItensRecebimentoPublic.update_forward_refs()

