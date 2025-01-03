# app/schemas/componente.py
from pydantic import BaseModel
from typing import List, Optional

from app.models.produto_tarefa import Produto_tarefa


class Produto_tarefaSchema(BaseModel):
    name: str


class Produto_tarefaPublic(Produto_tarefaSchema):
    id: int


class Produto_tarefaList(BaseModel):
    produto_tarefas: list[Produto_tarefaPublic]
    offset: int
    limit: int

class Produto_tarefaUpdate(BaseModel):
    name: str | None = None