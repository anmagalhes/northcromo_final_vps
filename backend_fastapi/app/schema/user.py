# app/shemas/user_schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from typing import List
from pydantic import BaseModel as SCBaseModel, EmailStr
from datetime import datetime

from app.schema.order_schem import OrderSchema

class UserSchemaBase(SCBaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    password: str
    en_admin: bool = False
    created_at: Optional[datetime]  # Data de criação (preenchida automaticamente)
    updated_at: Optional[datetime]  # Data de última atualização (preenchida automaticamente)

    class Config:
        from_attributes = True

class UserSchemaCreate(UserSchemaBase):
    password: str


class UsuarioSchemaGrupoProduto(UserSchemaBase):
    grupo_produtos:Optional[List[OrderSchema]]


class UserSchemaUP(UserSchemaBase):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    eh_admin: Optional[bool] = None

    class Config:
        from_attributes = True


    # You can also define schemas for the related 'GrupoProduto' model, if needed:

class GrupoProdutoSchema(SCBaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

class UserSchemaWithGrupoProduto(UserSchemaBase):
    grupo_produto: Optional[GrupoProdutoSchema]  # Include the related object

    class Config:
        from_attributes = True

class UserPublicSchema(UserSchemaBase):
    id: int
    username: str
    email: EmailStr
    nome: Optional[str] = None  # O campo 'nome' pode ser opcional
    eh_admin: Optional[bool] = None  # O campo 'eh_admin' pode ser opcional

    class Config:
        from_attributes = True

        