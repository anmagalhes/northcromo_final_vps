from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Produto_TaferaBase(BaseModel):
    produto_taf_nome: str = Field(..., example="Usinagem")
    data_execucao: Optional[datetime] = Field(
        default=None, description="Data e hora"
    )

    # Método para customizar a conversão de dados
    @classmethod
    def parse_obj(cls, obj):
        if "data_execucao" in obj and isinstance(obj["data_execucao"], str):
            obj["data_execucao"] = datetime.fromisoformat(obj["data_execucao"].replace("Z", "+00:00"))
        return super().parse_obj(obj)

class Produto_TaferaUpdate(BaseModel):
    produto_taf_nome: str
    data_execucao: datetime  # Obrigatório aqui

class Produto_TaferaCreate(Produto_TaferaBase):
    pass

class Produto_TaferaRead(Produto_TaferaBase):
    id: int

    model_config = {
        "from_attributes": True
    }
