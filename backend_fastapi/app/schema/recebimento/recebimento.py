# app/schemas/recebimento/recebimento.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.schema.variavel_global.enums import (
    TipoOrdemEnum,
    SimNaoEnum,
    StatusOrdemEnum,
    ProcessosOrdemEnum,
)
from app.schema.recebimento.itens_recebimento import ItensRecebimentoSchema
from app.schema.produto import ProdutoSchema


# Enum's do Pydantic (similares aos do SQLAlchemy)
class SimNaoEnum(str, Enum):
    SIM = "SIM"
    NAO = "NAO"


class TipoOrdemEnum(str, Enum):
    NOVO = "NOVO"
    NAO = "NAO"


class StatusOrdemEnum(str, Enum):
    PENDENTE = "PENDENTE"  # Status 1 - Pendente
    FINALIZADO = "FINALIZADO"  # Status 5 - Finalizado
    CANCELADO = "CANCELADO"  # Status 3 - Cancelado
    EM_ANDAMENTO = "EM_ANDAMENTO"


class StatusTarefaEnum(str, Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADO = "FINALIZADO"


# Esquema para criar um novo recebimento
class RecebimentoSchema(BaseModel):
    id: Optional[int] = None
    tipo_ordem: Optional[TipoOrdemEnum] = TipoOrdemEnum.NAO
    numero_ordem: Optional[int] = None
    recebimento_ordem: Optional[str] = None
    queixa_cliente: Optional[str] = None
    data_prazo_desmont: Optional[datetime] = None
    referencia_produto: Optional[str] = None
    numero_nota_fiscal: Optional[str] = None

    sv_desmontagem_ordem: SimNaoEnum = SimNaoEnum.NAO
    sv_montagem_teste_ordem: SimNaoEnum = SimNaoEnum.NAO
    limpeza_quimica_ordem: SimNaoEnum = SimNaoEnum.NAO
    laudo_tecnico_ordem: SimNaoEnum = SimNaoEnum.NAO
    desmontagem_ordem: SimNaoEnum = SimNaoEnum.NAO

    data_rec_ordem: datetime
    hora_inicial_ordem: Optional[datetime] = None
    data_final_ordem: Optional[datetime] = None
    hora_final_ordem: Optional[datetime] = None

    img1_ordem: Optional[str] = None
    img2_ordem: Optional[str] = None
    img3_ordem: Optional[str] = None
    img4_ordem: Optional[str] = None

    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    usuario_id: Optional[int] = None
    cliente_id: Optional[int] = None

    status_ordem: StatusOrdemEnum

    # Lista de itens que vão ser relacionados a esse recebimento
    itens: List["ItensRecebimentoSchema"]  # Usar string para Forward Reference


# Esquema para exibição pública de Recebimento
class RecebimentoPublic(RecebimentoSchema):
    id: int  # ID do recebimento no banco de dados


# Esquema para listagem de Recebimentos
class RecebimentoList(BaseModel):
    recebimentos: List[RecebimentoPublic]  # Lista de recebimentos
    offset: int  # Offset para paginação
    limit: int  # Limite para paginação


# Esquema para atualização de Recebimento
class RecebimentoUpdate(BaseModel):
    tipo_ordem: Optional[TipoOrdemEnum]  # Tipo de ordem (NOVO, NAO)
    numero_ordem: Optional[int]  # Número da ordem
    recebimento_ordem: Optional[str]  # Identificador da ordem de recebimento
    queixa_cliente: Optional[str]  # Queixa do cliente
    data_prazo_desmont: Optional[datetime]  # Prazo para desmontagem (usar datetime)

    sv_desmontagem_ordem: Optional[SimNaoEnum]  # Sim ou Não
    sv_montagem_teste_ordem: Optional[SimNaoEnum]  # Sim ou Não
    limpeza_quimica_ordem: Optional[SimNaoEnum]  # Sim ou Não
    laudo_tecnico_ordem: Optional[SimNaoEnum]  # Sim ou Não
    desmontagem_ordem: Optional[SimNaoEnum]  # Sim ou Não

    data_rec_ordem: Optional[datetime]  # Data do recebimento (usar datetime)
    hora_inicial_ordem: Optional[datetime]  # Hora inicial da ordem
    data_final_ordem: Optional[datetime]  # Data final da ordem
    hora_final_ordem: Optional[datetime]  # Hora final da ordem

    img1_ordem: Optional[str]  # Caminho para imagem 1
    img2_ordem: Optional[str]  # Caminho para imagem 2
    img3_ordem: Optional[str]  # Caminho para imagem 3
    img4_ordem: Optional[str]  # Caminho para imagem 4
    status_ordem: StatusOrdemEnum


class RecebimentoResponse(BaseModel):
    id: int
    tipo_ordem: TipoOrdemEnum
    numero_ordem: int
    recebimento_ordem: str
    queixa_cliente: str
    data_prazo_desmont: datetime
    sv_desmontagem_ordem: SimNaoEnum
    sv_montagem_teste_ordem: SimNaoEnum
    limpeza_quimica_ordem: SimNaoEnum
    laudo_tecnico_ordem: SimNaoEnum
    desmontagem_ordem: SimNaoEnum
    data_rec_ordem: datetime
    hora_inicial_ordem: Optional[datetime]
    data_final_ordem: datetime
    hora_final_ordem: datetime
    img1_ordem: Optional[str]
    img2_ordem: Optional[str]
    img3_ordem: Optional[str]
    img4_ordem: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    usuario_id: Optional[int]
    cliente_id: int
    status_ordem: StatusOrdemEnum

# Agora você pode importar as dependências no final do arquivo para evitar ciclo de importações
from app.schema.cliente import ClientePublic  # Agora importando ClientePublic
from app.schema.produto import ProdutoPublic
from app.schema.funcionario import FuncionarioPublic
from app.schema.checklist import ChecklistRecebimentoPublic

# Isso garante que as referências de "ClientePublic", "ProdutoPublic", etc., sejam resolvidas corretamente
RecebimentoPublic.update_forward_refs()
