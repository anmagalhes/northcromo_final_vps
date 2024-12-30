# app/controller/user.py
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from typing import Annotated, List, Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.schema.user import UserSchemaBase, UserSchemaCreate, UserSchemaUP, UserSchemaWithGrupoProduto, UserPublicSchema, UsuarioSchemaGrupoProduto

from pydantic import BaseModel
from datetime import timedelta, datetime, timezone

from core.desp import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

# GET LOGADO
@router.get('/logado',response_model=UserSchemaBase)
def get_logado(usuario_logado: User = Depends(get_current_user)):
    return  usuario_logado

# POST /signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_usuario(usuario: UserSchemaCreate, db: AsyncSession = Depends(get_session)):

    # Verifica se o username já existe
    stmt = select(User).filter(User.username == usuario.username)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Cria o novo usuário
    novo_usuario = User(
        username=usuario.username,
        email=usuario.email,
        password=gerar_hash_senha(usuario.password),  # Gera o hash da senha
        en_admin=usuario.en_admin
    )

    # Adiciona o novo usuário ao banco de dados
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)  # Atualiza o objeto com os dados persistidos

    # Retorna o novo usuário (sem a senha, pois estamos usando UserSchemaBase)
    return novo_usuario


@router.get('/users', response_model=List[UserSchemaBase])
async def get_usuarios(limit: int = 10, skip: int = 0, db: AsyncSession = Depends(get_session)):
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    users = result.scalars().all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )

    return users  # Retorna a lista de usuários com apenas username e email

@router.get('/users/{user_id}', response_model=UserPublicSchema)
async def get_usuario(user_id: int, db: AsyncSession = Depends(get_session)):
    # Consulta para buscar o usuário pelo ID
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()  # Retorna o primeiro usuário encontrado, ou None

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user  # Retorna o usuário com apenas os campos definidos em UserPublicSchema


@router.post("/register")
async def register_user(name: str, username: str, password: str):
    if not create_user(name, username, password):
        raise HTTPException(status_code=400, detail="Usuário já existe!")
    return {"message": "Usuário criado com sucesso!"}


@router.post("/login")
async def login(username: str, password: str):
    if not login_user(username, password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas!")
    return {"message": "Login bem-sucedido!"}
