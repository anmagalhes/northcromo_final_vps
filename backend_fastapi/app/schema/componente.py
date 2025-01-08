# app/schemas/componente.py
from pydantic import BaseModel, root_validator
from typing import List, Optional

from app.models.componente import Componente


class ComponenteSchema(BaseModel):
    name: str

    @root_validator(pre=True)
    def convert_to_uppercase(cls, values):
        # Itera sobre os campos e converte os valores do tipo str para maiúsculas
        for field, value in values.items():
            if isinstance(value, str):  # Verifica se o valor é uma string
                values[field] = value.upper()  # Converte para maiúsculas
        return values


class ComponentePublic(ComponenteSchema):
    id: int


class ComponenteList(BaseModel):
    componentes: list[ComponentePublic]
    offset: int
    limit: int


class ComponenteUpdate(BaseModel):
    name: str | None = None

    @root_validator(pre=True)
    def convert_to_uppercase(cls, values):
        # Itera sobre os campos e converte os valores do tipo str para maiúsculas
        for field, value in values.items():
            if isinstance(value, str):  # Verifica se o valor é uma string
                values[field] = value.upper()  # Converte para maiúsculas
        return values
