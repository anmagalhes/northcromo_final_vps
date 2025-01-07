# app/schemas/recebimento/itens_recebimento.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum


# Definindo o Enum de StatusOrdem
class StatusOrdemEnum(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    REJEITADO = "REJEITADO"


# Esquema básico para item de recebimento
class ItensRecebimentoSchema(BaseModel):
    qtd_produto: int  # Quantidade de produtos no item de recebimento
    preco_unitario: float  # Preço unitário
    preco_total: float  # Preço total (qtd_produto * preco_unitario)
    referencia_produto: Optional[str] = None  # Torna opcional
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
    referencia_produto: Optional[str] = None  # Torna opcional
    status_ordem: Optional[StatusOrdemEnum] = None


# Chame o update_forward_refs após a definição dos modelos
ItensRecebimentoPublic.update_forward_refs()
