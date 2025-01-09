from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime

from app.schema.produto import ProdutoSchema
from app.schema.funcionario import FuncionarioSchema


# Definindo o Enum de StatusOrdem com valores inteiros
class StatusOrdemEnum(str, Enum):
    PENDENTE = "PENDENTE"  # Status 1 - Pendente
    FINALIZADO = "FINALIZADO"  # Status 5 - Finalizado
    CANCELADO = "CANCELADO"  # Status 3 - Cancelado
    EM_ANDAMENTO = "EM_ANDAMENTO"  # Status 2 - Em andamento


# Esquema básico para item de recebimento
class ItensRecebimentoSchema(BaseModel):
    id: Optional[int] = None  # Tornando o id opcional
    qtd_produto: int  # Quantidade de produtos no item de recebimento
    preco_unitario: float  # Preço unitário
    preco_total: float  # Preço total (qtd_produto * preco_unitario)
    referencia_produto: Optional[str] = None  # Torna opcional
    status_ordem: StatusOrdemEnum  # Status do item de recebimento

    produto_id: int  # ID do produto relacionado
    recebimento_id: Optional[int] = None  # ID do recebimento relacionado
    funcionario_id: Optional[int] = None  # ID do funcionário relacionado (se houver)

    # Campos de controle de data
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Adicionando campo de fotos (uma lista de URLs de fotos, opcional)
    fotos: Optional[List[str]] = (
        []
    )  # Lista de URLs ou caminhos das fotos do item de recebimento

    # Incluindo informações adicionais do produto e funcionário, se necessário
    produto: Optional["ProdutoSchema"] = None
    funcionario: Optional["FuncionarioSchema"] = None  # Referência circular


# Inclusão do ID após a criação do item de recebimento
class ItensRecebimentoPublic(ItensRecebimentoSchema):
    id: int


# Exibição para usuário final com paginação
class ItensRecebimentoList(BaseModel):
    itensRecebimento: List[ItensRecebimentoPublic]
    offset: int
    limit: int


# Atualizar Item de Recebimento
class ItensRecebimentoUpdate(BaseModel):
    qtd_produto: Optional[int] = None
    preco_unitario: Optional[float] = None
    preco_total: Optional[float] = None
    referencia_produto: Optional[str] = None
    status_ordem: Optional[StatusOrdemEnum] = None
    fotos: Optional[List[str]] = None  # Permite atualizar a lista de fotos


# Chame o update_forward_refs após a definição dos modelos
def update_references():
    from app.schema.funcionario import (
        FuncionarioSchema,
    )  # Importação local para evitar circularidade

    ItensRecebimentoSchema.update_forward_refs()  # Atualizando a referência para FuncionarioSchema
    ItensRecebimentoPublic.update_forward_refs()  # Atualizando a referência para FuncionarioSchema


# Chame a função para atualizar as referências
update_references()
