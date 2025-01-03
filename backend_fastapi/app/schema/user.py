# app/shemas/user_schemas.py
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic import ConfigDict, EmailStr

from app.schema.order_schem import OrderSchema

import pytz

# Fuso horário de São Paulo
SP_TZ = pytz.timezone("America/Sao_Paulo")


class SCBaseModel(BaseModel):
    class Config:
        # Adiciona o comportamento padrão de conversão para json
        json_encoders = {
            datetime: lambda v: (
                v.astimezone(SP_TZ).isoformat() if v else None
            )  # Converte datetime para string ISO com o fuso horário de SP
        }


class UserSchemaBase(SCBaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    password: str
    en_admin: bool = False
    created_at: Optional[datetime]  # Data de criação (preenchida automaticamente)
    updated_at: Optional[
        datetime
    ]  # Data de última atualização (preenchida automaticamente)

    class Config:
        from_attributes = True


class UserSchemaCreate(UserSchemaBase):
    password: str


class UsuarioSchemaGrupoProduto(UserSchemaBase):
    grupo_produtos: Optional[List[OrderSchema]]


class UserSchemaUP(UserSchemaBase):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    eh_admin: Optional[bool] = None


class GrupoProdutoSchema(SCBaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class UserSchemaWithGrupoProduto(UserSchemaBase):
    grupo_produto: Optional[GrupoProdutoSchema]  # Include the related object

    class Config:
        from_attributes = True


class UserPublicSchema(SCBaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class TokenData(SCBaseModel):
    username: Optional[str] = None


class UserList(BaseModel):
    usuarios: list[UserPublicSchema]
    offset: int
    limit: int
