from datetime import datetime
from typing import Optional,  List
from pydantic import BaseModel
from app.api.models.enums import StatusTarefaEnum
from app.Schema.recebimento_schema import RecebimentoRead  # Você precisa garantir que existe

class TarefaBase(BaseModel):
    recebimento_id: int
    data_rec_ordem: datetime
    qtde_servico: int
    id_servico: int
    id_servico2: Optional[int] = None
    id_operacao: int
    desc_servico_produto: Optional[str] = None
    obs: Optional[str] = None
    status: Optional[StatusTarefaEnum] = StatusTarefaEnum.PENDENTE
    referencia_produto: Optional[str] = None
    nota_interna: Optional[str] = None
    data_checklist_ordem: Optional[datetime] = None

class TarefaCreate(TarefaBase):
    pass

class TarefaUpdate(BaseModel):
    data_rec_ordem: Optional[datetime]
    qtde_servico: Optional[int]
    id_servico: Optional[int]
    id_servico2: Optional[int]
    id_operacao: Optional[int]
    desc_servico_produto: Optional[str]
    obs: Optional[str]
    status: Optional[StatusTarefaEnum]
    referencia_produto: Optional[str]
    nota_interna: Optional[str]
    data_checklist_ordem: Optional[datetime]

class TarefaRead(TarefaBase):
    id: int
    data_lancamento: datetime
    created_at: datetime
    updated_at: datetime

    recebimento: Optional[RecebimentoRead]  # <- Aqui você acessa o cliente
    class Config:
        orm_mode = True

class PaginatedTarefas(BaseModel):
    data: List[TarefaRead]
    page: int
    limit: int
    total: int
    pages: int
