# No arquivo app/schemas/checklist_recebimento.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

from app.models.checklist_recebimento import checklist_recebimento


# Enum de Status da Tarefa
class StatusTarefaEnum(Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADO = "FINALIZADO"


# Esquema básico para checklist de recebimento
class ChecklistRecebimentoSchema(BaseModel):
    datarec_ordem_servicos: datetime  # Data da ordem de serviços
    hora_inicial_ordem: datetime  # Hora de início da ordem
    cod_produto: int  # Código do produto
    nota_interna: str  # Nota interna
    quantidade: int  # Quantidade de itens
    referencia_produto: str  # Referência do produto
    link: Optional[str] = None  # Link opcional para mais informações
    observacao_checklist: str  # Observação do checklist
    status_tarefa: StatusTarefaEnum = StatusTarefaEnum.PENDENTE  # Status da tarefa
    data_checklist_ordem_servicos: datetime  # Data do checklist

    cliente_id: int  # ID do cliente associado
    usuario_id: Optional[int] = None  # ID do usuário responsável (opcional)
    recebimento_id: Optional[int] = None  # ID do recebimento associado (opcional)


# Inclusão do ID após a criação do checklist
class ChecklistRecebimentoPublic(ChecklistRecebimentoSchema):
    id: int  # ID do checklist
    # cliente: Optional["ClientePublic"]  # Cliente completo (relacionado) - Usando Forward Reference
    # usuario: Optional["UserPublicSchema"]  # Usuário responsável, se houver - Usando Forward Reference
    # recebimento: Optional["RecebimentoPublic"]  # Recebimento completo, se houver - Usando Forward Reference


# Exibição para listagem de checklists (com paginação)
class ChecklistRecebimentoList(BaseModel):
    checklists: list[ChecklistRecebimentoPublic]
    offset: int
    limit: int


# Criar Novo Checklist de Recebimento
class ChecklistRecebimentoCreate(BaseModel):
    datarec_ordem_servicos: datetime  # Data da ordem de serviços
    hora_inicial_ordem: datetime  # Hora de início da ordem
    cod_produto: int  # Código do produto
    nota_interna: str  # Nota interna
    quantidade: int  # Quantidade de itens
    referencia_produto: str  # Referência do produto
    link: Optional[str] = None  # Link opcional para mais informações
    observacao_checklist: str  # Observação do checklist
    status_tarefa: StatusTarefaEnum = StatusTarefaEnum.PENDENTE  # Status da tarefa
    data_checklist_ordem_servicos: datetime  # Data do checklist

    cliente_id: int  # ID do cliente associado
    usuario_id: Optional[int] = None  # ID do usuário responsável (opcional)
    recebimento_id: Optional[int] = None  # ID do recebimento associado (opcional)


# Atualizar Checklist de Recebimento
class ChecklistRecebimentoUpdate(BaseModel):
    datarec_ordem_servicos: Optional[datetime] = None
    hora_inicial_ordem: Optional[datetime] = None
    cod_produto: Optional[int] = None
    nota_interna: Optional[str] = None
    quantidade: Optional[int] = None
    referencia_produto: Optional[str] = None
    link: Optional[str] = None
    observacao_checklist: Optional[str] = None
    status_tarefa: Optional[StatusTarefaEnum] = None
    data_checklist_ordem_servicos: Optional[datetime] = None

# Representação de um Checklist simples para exibição
class ChecklistSimple(BaseModel):
    id: int
    nota_interna: str
    referencia_produto: str
    status_tarefa: str
    impresso: bool

# Para representar o retorno de um checklist impresso ou qualquer outra ação simples.
class ChecklistPrintStatus(BaseModel):
    id: int
    impresso: bool  # Se foi impresso ou não


# Exemplo de resposta para o checklist com dados completos
class ChecklistFullResponse(BaseModel):
    id: int
    nota_interna: str
    referencia_produto: str
    status_tarefa: str
    observacao_checklist: Optional[str] = None
    hora_inicial_ordem: Optional[str] = None
    datarec_ordem_servicos: datetime
    usuario_id: int
    impresso: bool
    criado_em: datetime

# Atualizar as referências para tipos relacionados
ChecklistRecebimentoPublic.update_forward_refs()
