from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi import Depends

DATABASE_URL = "sqlite+aiosqlite:///./database.db"  # Para SQLite assíncrono
SYNC_DATABASE_URL = "sqlite:///./database.db"

# Async engine (para FastAPI async)
async_engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Função para ser usada com Depends (async)
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Sync engine (para compatibilidade com partes legadas)
sync_engine = create_engine(SYNC_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
