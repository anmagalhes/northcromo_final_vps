from pydantic_settings import BaseSettings
from pydantic import validator
from dotenv import load_dotenv
from typing import List, Optional
import secrets
from pydantic import Extra

# Carrega as variáveis do arquivo .env
load_dotenv()

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./database.db"
    ASYNC_DATABASE_URL: Optional[str] = None  # Declara explicitamente para ser lido pelo Pydantic

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
    "extra": "ignore"  # importante para ignorar variáveis extras no .env
}

    @validator("ASYNC_DATABASE_URL", pre=True, always=True)
    def build_async_database_url(cls, v, values):
        # Se a variável ASYNC_DATABASE_URL estiver definida no .env, usa ela
        if v is not None:
            return v
        # Se não, cria baseada na DATABASE_URL
        database_url = values.get("DATABASE_URL", "")
        if database_url.startswith("sqlite://"):
            return database_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
        return database_url

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

# Cria uma instância única de configurações que será usada em todo o projeto
settings = Settings()

# Validação simples para impedir SQLite em produção
if settings.is_production:
    if "sqlite" in settings.ASYNC_DATABASE_URL:
        raise ValueError("SQLite não é permitido em produção")
