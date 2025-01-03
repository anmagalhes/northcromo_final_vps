# app/schemas/componente.py
from pydantic import BaseModel
from typing import List, Optional

from app.models.componente import Componente


class ComponenteSchema(BaseModel):
    name: str


class ComponentePublic(ComponenteSchema):
    id: int


class ComponenteList(BaseModel):
    componentes: list[ComponentePublic]
    offset: int
    limit: int


class ComponenteUpdate(BaseModel):
    name: str | None = None
