# models/user.py
from typing import Optional
from pydantic import BaseModel as SCBaseModel
from datetime import datetime

class UserSchema(SCBaseModel):
    id: Optional(int)
    username:str
    email:str
    password:str
    created_at: Optional[datetime]  # Data de criação (preenchida automaticamente)
    updated_at: Optional[datetime]  # Data de última atualização (preenchida automaticamente)

class Config:
    orm_mode = True