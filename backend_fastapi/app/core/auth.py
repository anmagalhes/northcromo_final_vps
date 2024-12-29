# app/core/auth.py
from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt, JWTError

from ..models.user import User
from ..core.config import settings
from ..core.security import verificar_senha

from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)


async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[User]:
    async with db as session:
        query = select(User).filter(User.email == email)
        result = await session.execute(query)
        usuario: User = result.scalars().unique().one_or_none()

        if not usuario:
            return None

        if not verificar_senha(senha, usuario.senha):
            return None
        return usuario


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # Inicializando o payload
    payload = {}

    # Definindo o fuso horário de São Paulo
    sp = timezone('America/Sao_Paulo')

    # Calculando o tempo de expiração do token
    expira = datetime.now(tz=sp) + tempo_vida  # Tempo atual + tempo de vida do token

    # Adicionando as informações ao payload
    payload["type"] = tipo_token  # Tipo do token (ex: access_token, refresh_token)
    payload["exp"] = expira  # Expiração do token
    payload["iat"] = datetime.now(tz=sp)  # Data de emissão (now)
    payload["sub"] = str(sub)  # Subject (usuário ou identificador único)

    # Assinando o token com o segredo (JWT_SECRET) e o algoritmo (HS256)
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

    return token


def criar_token_acesso(sub: str) -> str:
    return _criar_token(
        tipo_token='access_token',  # Tipo do token
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),  # Correção de "minutos" para "minutes"
        sub=sub  # Subject do token (geralmente o ID do usuário ou outra chave única)
    )
