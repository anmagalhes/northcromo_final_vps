from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

db_url = settings.async_database_url  # Garante que seja async (com +asyncpg se necessário)

print("URL do banco usada tony:", db_url)

# 🚧 Criação do engine depende do tipo de banco
if "sqlite" in db_url:
    engine = create_async_engine(
        db_url,
        echo=settings.ENVIRONMENT == "development",
        connect_args={"check_same_thread": False},
        poolclass=NullPool  # Para evitar locks em SQLite
    )
else:
    engine = create_async_engine(
        db_url,
        echo=settings.ENVIRONMENT == "development",
        poolclass=NullPool  # 🔧 Evita problemas com Supabase ou pools no deploy inicial
    )

# 📦 Session factory assíncrona
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# ⚙️ Função para obter sessões de banco de dados
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        if "sqlite" in db_url:
            await session.execute("PRAGMA foreign_keys=ON")

        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
