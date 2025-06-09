#app/Schema/defeitos_schema.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class DefeitoBase(BaseModel):
    id: Optional[int] = None
    data: Optional[datetime] = None
    componente_id: int = Field(..., description="ID do componente associado")
    def_nome: str = Field(..., max_length=100, description="Nome do defeito")

    @validator("def_nome", pre=True, always=True)
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

    @validator("data", pre=True, always=True)
    def parse_data(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except Exception:
                raise ValueError("data deve ser uma string ISO 8601 válida")
        return v

    class Config:
        orm_mode = True


class DefeitoCreate(DefeitoBase):
    pass

class DefeitoRead(DefeitoBase):
    id: int
    def_nome: str
    data: datetime
    componente_id: int
    componente_nome: Optional[str]  # <- Adicionado

    class Config:
        orm_mode = True


