# app/schemas/Operacao.py
from pydantic import BaseModel
from typing import List, Optional
from app.models.operacao import Operacao


class OperacaoSchema(BaseModel):
    name: str
    grupo_operacao: str


class OperacaoPublic(OperacaoSchema):
    id: int


class OperacaoList(BaseModel):
    Operacaos: List[OperacaoPublic]
    offset: int
    limit: int


class OperacaoUpdate(BaseModel):
    name: Optional[str] = None
    grupo_operacao: Optional[str] = None

