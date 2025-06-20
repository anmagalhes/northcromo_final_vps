from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OperacaoBase(BaseModel):
    op_grupo_processo: str = Field(..., example="Usinagem")
    op_nome: str = Field(..., example="Fresagem")
    data_execucao: Optional[datetime] = Field(
        default=None, description="Data e hora"
    )



class OperacaoCreate(OperacaoBase):
    pass

class OperacaoRead(OperacaoBase):
    id: int

    model_config = {
        "from_attributes": True
    }
