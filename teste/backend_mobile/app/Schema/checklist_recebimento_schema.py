# app/schemas/checklist_recebimento.py

from pydantic import BaseModel
from typing import Optional

class ChecklistRecebimentoBase(BaseModel):
    recebimento_id: int
    item1: Optional[bool] = False
    item2: Optional[bool] = False
    observacoes: Optional[str] = None
    link_pdf: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class ChecklistRecebimentoCreate(ChecklistRecebimentoBase):
    pass

class ChecklistRecebimentoRead(ChecklistRecebimentoBase):
    id: int

    model_config = {
        "from_attributes": True
    }
