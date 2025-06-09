from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class ComponenteSchema(BaseModel):
    componente_nome: Optional[str] = Field(
        default=None, max_length=25, description="Nome do componente"
    )

    data_recebimento: Optional[datetime] = Field(
        default=None, description="Data e hora de recebimento"
    )

    @validator("componente_nome", pre=True)
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class ComponenteCreate(ComponenteSchema):
    pass  # futuro uso: validação extra, campos obrigatórios, etc.


class ComponenteRead(ComponenteSchema):
    id: int

    model_config = {
        "from_attributes": True
    }
