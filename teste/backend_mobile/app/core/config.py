from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List, Optional
import secrets

#load_dotenv()
class Settings(BaseSettings):
    ENVIRONMENT: str = "development"

    # Para Supabase, a URL deve usar asyncpg para SQLAlchemy async
    DATABASE_URL: str  # ex: postgresql+asyncpg://user:pass@host:port/dbname
    ASYNC_DATABASE_URL: Optional[str] = None  # Se quiser sobrescrever, caso contrário será igual a DATABASE_URL

    JWT_SECRET: str = secrets.token_urlsafe(64)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 2

    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://seusite.com"]

    SENTRY_DSN: Optional[str] = None
    MAINTENANCE_ALERT_DAYS: int = 7
    MAX_FILE_UPLOAD_SIZE_MB: int = 10

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }

    @property
    def async_database_url(self) -> str:
        # Retorna ASYNC_DATABASE_URL se estiver setada, senão DATABASE_URL
        return self.ASYNC_DATABASE_URL or self.DATABASE_URL

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

# Instância global das configurações
settings = Settings()

# Validação para impedir usar SQLite em produção — aqui opcional pois não usaremos SQLite
if settings.is_production and "sqlite" in settings.async_database_url:
    raise ValueError("SQLite não é permitido em produção")
