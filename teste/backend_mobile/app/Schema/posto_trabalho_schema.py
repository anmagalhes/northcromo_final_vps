# app/Schema/posto_trabalho.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Posto_TrabalhoBase(BaseModel):
    posto_trabalho_nome: str = Field(..., example="Usinagem")
    data_execucao: Optional[datetime] = Field(
        default=None, description="Data e hora"
    )

class Posto_TrabalhoUpdate(BaseModel):
    posto_trabalho_nome: str
    data_execucao: datetime  # Obrigatório aqui

class Posto_TrabalhoCreate(Posto_TrabalhoBase):
    pass

class Posto_TrabalhoRead(Posto_TrabalhoBase):
    id: int

    model_config = {
        "from_attributes": True
    }
