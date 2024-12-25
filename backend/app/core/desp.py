# app/cors/desp.py
from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Session  # Certifique-se de que Session está importado corretamente

# Função para obter a sessão assíncrona do banco de dados
async def get_session() -> Generator[AsyncSession, None, None]:
    async with Session() as session:  # Usando async with para garantir que a sessão seja fechada automaticamente
        yield session  # A sessão é gerada para ser utilizada na dependência
