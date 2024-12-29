from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Session  # Assumindo que você tenha um Session configurado corretamente

# Função para obter a sessão assíncrona
async def get_session() -> Generator:
    """
    Função geradora que cria uma sessão assíncrona com o banco de dados, 
    a utiliza para operações e fecha ao final.
    """
    session: AsyncSession = Session()

    try:
        # A sessão é gerada para uso externo
        yield session
    finally:
        # Garante que a sessão seja fechada após o uso
        await session.close()
