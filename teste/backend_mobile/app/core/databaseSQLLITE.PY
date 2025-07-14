# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.base_class import Base
from app.core.config import settings

db_url = settings.ASYNC_DATABASE_URL

if "sqlite" in db_url:
    engine = create_async_engine(
        db_url,
        echo=settings.ENVIRONMENT == "development",
        connect_args={"check_same_thread": False},
        poolclass=NullPool
    )
else:
    engine = create_async_engine(
        db_url,
        echo=settings.ENVIRONMENT == "development",
        pool_size=20,
        max_overflow=10,
        pool_timeout=30
    )

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

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
