# app/schemas/funcionario.py
from pydantic import BaseModel
from typing import Optional, List

class FuncionarioSchema(BaseModel):
    name: str
    email: Optional[str] = None

class FuncionarioPublic(FuncionarioSchema):
    id: int

class FuncionarioList(BaseModel):
    Funcionarios: list[FuncionarioPublic]
    offset: int
    limit: int


class FuncionarioUpdate(BaseModel):
    name: str | None = None

