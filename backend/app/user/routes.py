# Importando as funções de `services.py` localizado em `app/user/`
from app.user.services import create_user, login_user
from fastapi import APIRouter, HTTPException
from typing import List

users_router = APIRouter()

@users_router.get("/", response_model=List[str])
async def get_users():
    return ["user1", "user2", "user3"]

@users_router.post("/register")
async def register_user(name: str, username: str, password: str):
    if not create_user(name, username, password):
        raise HTTPException(status_code=400, detail="Usuário já existe!")
    return {"message": "Usuário criado com sucesso!"}

@users_router.post("/login")
async def login(username: str, password: str):
    if not login_user(username, password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas!")
    return {"message": "Login bem-sucedido!"}
