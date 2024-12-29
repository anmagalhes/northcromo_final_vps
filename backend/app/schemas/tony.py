# app/schemas/tony.py
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List

from pydantic import BaseModel, EmailStr
from typing import List

# Pydantic Schema para o User - usado para criação de usuário
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

# Pydantic Schema para retornar um usuário completo do banco de dados
class UserBD(UserSchema):
    id: int

    class Config:
        from_attributes = True  # Permite que o Pydantic aceite objetos do tipo ORM (SQLModel)

# Modelo simplificado para exibir informações públicas do usuário
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    class Config:
        from_attributes = True

# Lista de usuários com o modelo UserPublic
class UserList(BaseModel):
    users: List[UserPublic]

# Mensagens personalizadas
class Tony(BaseModel):
    message: str
    bata: str
