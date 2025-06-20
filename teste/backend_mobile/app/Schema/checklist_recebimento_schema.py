from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

from app.Schema.componente_schema import ComponenteRead
from app.Schema.operacao_schema import OperacaoRead
from app.Schema.posto_trabalho_schema import Posto_TrabalhoRead
from app.Schema.recebimento_schema import RecebimentoRead

class BaseSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }

class ChecklistRecebimentoBase(BaseSchema):
    recebimento_id: int
    item1: Optional[bool] = False
    item2: Optional[bool] = False
    observacoes: Optional[str] = None
    link_pdf: Optional[str] = None

class ChecklistRecebimentoCreate(ChecklistRecebimentoBase):
    pass

class ChecklistRecebimentoRead(ChecklistRecebimentoBase):
    id: int
    os_formatado: Optional[str] = None
    recebimento: Optional["RecebimentoRead"] = None

    # Relacionamentos carregados - agora opcionais
    componente: Optional[ComponenteRead] = None
    operacao: Optional[OperacaoRead] = None
    posto_trabalho: Optional[Posto_TrabalhoRead] = None

class ChecklistRecebimentoUpdate(BaseSchema):
    item1: Optional[bool] = None
    item2: Optional[bool] = None
    observacoes: Optional[str] = None
    link_pdf: Optional[str] = None
