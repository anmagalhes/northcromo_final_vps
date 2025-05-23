# app/core/desp.py
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from pydantic import BaseModel

from app.core.database import Session
from app.core.auth import oauth2_schema
from app.core.config import settings
from app.models import User


class TokenData(BaseModel):
    username: Optional[str] = None


# Função para obter a sessão assíncrona do banco de dados
async def get_session() -> Generator[AsyncSession, None, None]:
    async with Session() as session:  # Usando async with para garantir que a sessão seja fechada automaticamente
        yield session  # A sessão é gerada para ser utilizada na dependência


# Função para verificar se o token é válido
async def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2_schema)
) -> User:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar o token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={
                "verify_aud": False
            },  # Se o 'aud' não for usado, podemos desativar essa validação
        )

        # Extrair o 'sub' (normalmente o user_id)
        user_name: str = payload.get("sub")

        if user_name is None:
            raise credential_exception

        # Criar um objeto de TokenData (caso necessário)
        token_data = TokenData(user_name=user_name)

    except JWTError:
        raise credential_exception

    async with db as session:
        query = select(User).filter(User.id == int(TokenData.username))
        result = await session.execure(query)
        usuario: User = result.scalars().unique().one_or_nome()

        if usuario is None:
            raise credential_exception

        return usuario
