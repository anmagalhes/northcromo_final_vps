from typing import Optional
from datetime import datetime, timedelta, timezone as dt_timezone

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from pydantic import EmailStr

from ..models.user import User
from ..core.config import settings
from ..core.security import verificar_senha  # Sua função para validar hash de senha

# OAuth2 URL para login — ajustar a rota conforme sua API
oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/usuarios/login")


async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[User]:
    # Busca o usuário pelo email
    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    usuario: User = result.scalars().unique().one_or_none()

    if not usuario:
        return None

    # Verifica se a senha bate com o hash salvo
    if not verificar_senha(senha, usuario.senha):
        return None

    return usuario


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # Usa UTC para datas no token (padrão JWT)
    agora = datetime.now(tz=dt_timezone.utc)
    expira = agora + tempo_vida

    payload = {
        "type": tipo_token,
        "exp": expira,
        "iat": agora,
        "sub": str(sub),
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def criar_token_acesso(sub: str) -> str:
    return _criar_token(
        tipo_token="access_token",
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def criar_token_refresh(sub: str) -> str:
    return _criar_token(
        tipo_token="refresh_token",
        tempo_vida=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


async def validar_token(token: str) -> Optional[str]:
    """
    Valida o token JWT, retorna o 'sub' (usuário) se válido,
    ou None se inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
