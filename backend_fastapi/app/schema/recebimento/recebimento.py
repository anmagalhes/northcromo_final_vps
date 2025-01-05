from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schema.produto import ProdutoResponse
from .checklist import ChecklistResponse
from .cliente import ClienteResponse
from .vendedor import VendedorResponse
from .enums import TipoOrdemEnum, SimNaoEnum, StatusOrdemEnum, ProcessosOrdemEnum


# Esquema para criar um novo recebimento
class RecebimentoSchema(BaseModel):
    tipo_ordem: TipoOrdemEnum
    numero_ordem: int
    recebimento_ordem: str
    data_rec_ordem: datetime
    queixa_cliente: str
    data_prazo_desmont: datetime
    sv_desmontagem_ordem: SimNaoEnum = SimNaoEnum.NAO
    sv_montagem_teste_ordem: SimNaoEnum = SimNaoEnum.NAO
    limpeza_quimica_ordem: SimNaoEnum = SimNaoEnum.NAO
    laudo_tecnico_ordem: SimNaoEnum = SimNaoEnum.NAO
    desmontagem_ordem: SimNaoEnum = SimNaoEnum.NAO

    # Relacionamento com outros objetos através dos IDs
    cliente_id: int  # ID do cliente
    vendedor_id: Optional[int] = None  # ID do vendedor (opcional)
    
    # Lista de itens que vão ser relacionados a esse recebimento
    itens_recebimento: List["ItensRecebimentoCreate"]  # Você pode definir o schema do item se necessário.

    class Config:
        orm_mode = True  # Garantir que o Pydantic possa converter SQLAlchemy em Pydantic (e vice-versa)

class RecebimentoPublic(RecebimentoSchema):
    id: int  # ID do recebimento no banco de dados

    cliente: ClienteResponse  # Detalhes do cliente (relacionado)
    produtos: List[ProdutoResponse]  # Lista de produtos relacionados ao recebimento
    vendedor: Optional[VendedorResponse]  # Detalhes do vendedor (opcional)
    ordem_checklist: List[ChecklistResponse]  # Lista de checklists relacionados
    status_ordem: StatusOrdemEnum  # Status da ordem
    processos_ordem: ProcessosOrdemEnum  # Processo da ordem

    # Outros campos que podem ser retornados
    data_producao_ordem_servicos: datetime
    sv_desmontagem_ordem: SimNaoEnum
    sv_montagem_teste_ordem: SimNaoEnum
    limpeza_quimica_ordem: SimNaoEnum
    laudo_tecnico_ordem: SimNaoEnum
    desmontagem_ordem: SimNaoEnum
    data_cadastro: datetime
    usuario_cadastro: str
    status_producao: Optional[str]
    num_orcamento: Optional[str]
    acao: Optional[str]

    class Config:
        orm_mode = True  # Permite que o Pydantic converta objetos ORM em modelos Pydantic
