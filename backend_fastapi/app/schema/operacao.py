# app/schemas/Operacao.py
from pydantic import BaseModel, root_validator
from typing import List, Optional
from app.models.operacao import Operacao


class OperacaoSchema(BaseModel):
    name: str
    grupo_operacao: str

    @root_validator(pre=True)
    def convert_to_uppercase(cls, values):
        # Itera sobre os campos e converte os valores do tipo str para maiúsculas
        # 'values' é um dicionário que contém os campos que estamos recebendo para criar a instância
        for field in values:
            value = values[field]
            if isinstance(value, str):  # Verifica se o valor é uma string
                values[field] = value.upper()  # Converte para maiúsculas
        return values


class OperacaoPublic(OperacaoSchema):
    id: int


class OperacaoList(BaseModel):
    Operacaos: List[OperacaoPublic]
    offset: int
    limit: int


class OperacaoUpdate(BaseModel):
    name: Optional[str] = None
    grupo_operacao: Optional[str] = None

    @root_validator(pre=True)
    def convert_to_uppercase(cls, values):
        # Itera sobre os campos e converte os valores do tipo str para maiúsculas
        for field in values:
            value = values[field]
            if isinstance(value, str):  # Verifica se o valor é uma string
                values[field] = value.upper()  # Converte para maiúsculas
        return values
