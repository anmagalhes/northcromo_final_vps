# app/schemas/funcionario.py
from pydantic import BaseModel
from typing import Optional, List
from app.models.funcionario import Funcionario


# Esquema básico para Funcionario
class FuncionarioSchema(BaseModel):
    nome: str  # Nome do funcionário
    cargo: str  # Cargo do funcionário


# Esquema de Funcionario para exibição pública (com relacionamentos)
class FuncionarioPublic(FuncionarioSchema):
    id: int  # ID do funcionário


# Exibição de múltiplos funcionários (com paginação)
class FuncionarioList(BaseModel):
    funcionarios: List[FuncionarioPublic]  # Lista de funcionários
    offset: int  # Offset da paginação
    limit: int  # Limite da paginação


# Esquema para criação de novo Funcionario
class FuncionarioCreate(FuncionarioSchema):
    pass


# Esquema para atualização de Funcionario
class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = None  # Nome do funcionário
    cargo: Optional[str] = None  # Cargo do funcionário


# Atualiza as referências de tipo após a definição
FuncionarioPublic.update_forward_refs()
