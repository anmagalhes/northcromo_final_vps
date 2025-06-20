from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FuncaoBase(BaseModel):
    funcao_nome: str = Field(..., example="Vendedor")
    descricao: Optional[str] = Field(None, example="Responsável pelas vendas e atendimento ao cliente")
    data_cadastro: Optional[datetime]

class FuncaoCreate(FuncaoBase):
    pass

class FuncaoUpdate(BaseModel):
    funcao_nome: Optional[str] = Field(None, example="Mecânico")
    descricao: Optional[str] = Field(None, example="Responsável pela manutenção dos veículos")

class FuncaoRead(FuncaoBase):
    id: int
    data_cadastro: Optional[datetime]  # vem do TimestampMixin

    model_config = {
        "from_attributes": True
    }
