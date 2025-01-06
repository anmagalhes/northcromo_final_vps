# app/schemas/recebimento/recebimento.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.schema.variavel_global.enums import TipoOrdemEnum, SimNaoEnum, StatusOrdemEnum, ProcessosOrdemEnum
from app.schema.recebimento.itens_recebimento import ItensRecebimentoSchema

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
    itens_recebimento: List["ItensRecebimentoSchema"]  # Usar string para Forward Reference


# Esquema para exibição pública de Recebimento
class RecebimentoPublic(RecebimentoSchema):
    id: int  # ID do recebimento no banco de dados

    cliente: Optional["ClientePublic"]  # Usando Forward Reference
    produtos: List["ProdutoPublic"]
    vendedor: Optional["FuncionarioPublic"]
    ordem_checklist: List["ChecklistRecebimentoPublic"]
    status_ordem: "StatusOrdemEnum"  # Usando a referência adiada corretamente
    processos_ordem: "ProcessosOrdemEnum"  # Da mesma forma

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

# Agora você pode importar as dependências no final do arquivo para evitar ciclo de importações
from app.schema.cliente import ClientePublic  # Agora importando ClientePublic
from app.schema.produto import ProdutoPublic
from app.schema.funcionario import FuncionarioPublic
from app.schema.checklist import ChecklistRecebimentoPublic

# Isso garante que as referências de "ClientePublic", "ProdutoPublic", etc., sejam resolvidas corretamente
RecebimentoPublic.update_forward_refs()
