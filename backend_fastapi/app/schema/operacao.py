# app/schemas/Operacao.py
from pydantic import BaseModel
from typing import List, Optional

from app.models.operacao import Operacao

class OperacaoSchema(BaseModel):
    name: str

class OperacaoPublic(OperacaoSchema):
    id: int

class OperacaoList(BaseModel):
    Operacaos: list[OperacaoPublic]
    offset: int
    limit: int

class OperacaoUpdate(BaseModel):
    name: str | None = None