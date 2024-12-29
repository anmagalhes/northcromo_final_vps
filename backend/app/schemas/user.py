# app/shemas/user_schemas.py
from typing import Optional
from typing import List
from pydantic import BaseModel as SCBaseModel, EmailStr
from datetime import datetime


class UserSchemaBase(SCBaseModel):
    id: Optional[int] = None
    username:str
    email:EmailStr
    password:str
    en_admin: bool = False
    created_at: Optional[datetime]  # Data de criação (preenchida automaticamente)
    updated_at: Optional[datetime]  # Data de última atualização (preenchida automaticamente)

class Config:
    orm_mode = True

class UserSchemaCreate(UserSchemaBase):
    password: str

#class UserSchemaArtigos(UserSchemaBase):
 #   cliente: Optional [List[cliente]]

class UserSchemaUP(UserSchemaBase):
    nome:Optional[str]  = None
    email:Optional[EmailStr] = None
    password:Optional[str]= None
    eh_admin: Optional[bool] = None


    # You can also define schemas for the related 'GrupoProduto' model, if needed:
class GrupoProdutoSchema(SCBaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True

class UserSchemaWithGrupoProduto(UserSchemaBase):
    grupo_produto: Optional[GrupoProdutoSchema]  # Include the related object

    class Config:
        orm_mode = True





