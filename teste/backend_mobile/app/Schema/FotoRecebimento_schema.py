# app/schemas/foto_recebimento_schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FotoRecebimentoBase(BaseModel):
    id_ordem: str
    nome_foto: str


class FotoRecebimentoCreate(FotoRecebimentoBase):
    pass


class FotoRecebimentoUpdate(FotoRecebimentoBase):
    pass


class FotoRecebimentoInDB(FotoRecebimentoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = (
            True  # Permite a conversão automática de objetos SQLAlchemy para Pydantic
        )

class LinksFotos(BaseModel):
    numero_ordem: str  # vem como string do frontend
    foto1: str
    foto2: str
    foto3: str
    foto4: str
    cliente: str
    quantidade: int
