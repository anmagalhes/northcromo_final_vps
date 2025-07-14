from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("ASYNC_DATABASE_URL") # Supabase URL

# Async engine para PostgreSQL (Supabase)
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Async sessionmaker
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Função para usar no Depends
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
