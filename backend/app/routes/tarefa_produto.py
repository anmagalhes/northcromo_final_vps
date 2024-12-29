# app/routes/cliente.py
from typing import List
from http import HTTPStatus 
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

#from app.models.cliente_model import Cliente
#from app.models.user import User
# Importe a classe Tony de app.schemas.tony
from app.schemas.tony import (
    Tony, UserSchema, UserPublic, UserBD, UserList)

from app.core.desp import get_session, get_current_user

# BYpass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

# Corrigindo o nome do método `inherit_cache` (ao invés de `inrerit_cache`)
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
# Fim BYpass

tarefa_produto_router = APIRouter()

database = []

@tarefa_produto_router.get('/', status_code=HTTPStatus.OK, response_model=Tony)  # Use a classe Tony diretamente
def red_root():
    return {'message': 'teste','bata':'A'}

# Criar no banco
@tarefa_produto_router.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def creater_user(user: UserSchema):

    user_with_id = UserBD(
        id = len(database) + 1,

        ## CRIAR UM DICIONARIO EM PYTHON
        **user.model_dump()
    )

    database.append(user_with_id)

    return user_with_id

# Lista no Banco
@tarefa_produto_router.get('/users/', response_model=UserList)
def read_users():
    return{'users':database}


"""
    > {user_id}: Criar uma "variável" na url
    > user_id: int: 
    """

#Alterar Registro
@tarefa_produto_router.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user:UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    
    # Atualizando o usuário no banco de dados fictício
    user_with_id = UserBD(
        id=user_id,
        **user.model_dump())
    database[user_id - 1] = user_with_id

    return user_with_id

@tarefa_produto_router.delete('/users/{user_id}', response_model=UserPublic)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    user_with_id  = database[user_id - 1]
    del database[user_id - 1]

    return {'messege': user_with_id}
