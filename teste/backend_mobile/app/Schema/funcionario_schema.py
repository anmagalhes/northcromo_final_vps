from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.Schema.funcao_schema import FuncaoRead
from typing import Literal
from app.api.models.enums import StatusEnum  # importe o enum correto

class FuncionarioBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    funcao_id: int
    acesso_sistema: bool = False
    status: StatusEnum
    data_cadastro: datetime

class FuncionarioCreate(FuncionarioBase):
    usuario_id: Optional[int] = None

class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    funcao_id: Optional[int] = None
    acesso_sistema: Optional[bool] = None
    usuario_id: Optional[int] = None
    data_cadastro:  Optional[datetime] = None


class FuncionarioRead(FuncionarioBase):
    id: int
    data_cadastro: datetime
    usuario_id: Optional[int] = None
    funcao_rel: Optional[FuncaoRead] = None  # relacionamento com função

    model_config = {
        "from_attributes": True
    }
