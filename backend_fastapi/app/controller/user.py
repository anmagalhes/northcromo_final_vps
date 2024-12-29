# Importando as funções de `services.py` localizado em `app/user/`
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.security import OAu
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.schema.user import UserSchemaBase, UserSchemaCreate, UserSchemaUP, UserSchemaWithGrupoProduto

api_router = APIRouter()


@api_router.get("/", response_model=List[str])
async def get_users():
    return ["user1", "user2", "user3"]


@api_router.post("/register")
async def register_user(name: str, username: str, password: str):
    if not create_user(name, username, password):
        raise HTTPException(status_code=400, detail="Usuário já existe!")
    return {"message": "Usuário criado com sucesso!"}


@api_router.post("/login")
async def login(username: str, password: str):
    if not login_user(username, password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas!")
    return {"message": "Login bem-sucedido!"}
