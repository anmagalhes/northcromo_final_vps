# app/cors/config.py
from typing import List
from typing import ClassVar
from pathlib import Path
import secrets
from datetime import datetime, timedelta
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

from pathlib import Path
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Verifique se as variáveis estão sendo carregadas corretamente
print(os.getenv("DATABASE_HOST"))


class Settings(BaseSettings):
    Base: ClassVar = declarative_base()

    # Variáveis de ambiente para conexão com o banco de dados
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str


    print("DATABASE_USER:", os.getenv("DATABASE_USER"))
    print("DATABASE_PASSWORD:", os.getenv("DATABASE_PASSWORD"))
    print("DATABASE_HOST:", os.getenv("DATABASE_HOST"))
    print("DATABASE_PORT:", os.getenv("DATABASE_PORT"))
    print("DATABASE_NAME:", os.getenv("DATABASE_NAME"))

    # Configurações de API e log
    API_V1_STR: str = "/api/V1"  # Rota base da API
    VITE_API_URL: str = "https://northcromocontrole.com.br/api"
    LOG_LEVEL: str = "INFO"

    JWT_SECRET: str = 'Dx4SYMqfpuMfy1NN-TKEOHm6Sx0TfhSOkgmL0tZ_XSU'
    """
    import secret
    token str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'
    # Validação token o tempo
    ACESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 365  # 1 ano

    class Config:
        env_file = ".env"  # O arquivo .env será carregado automaticamente
        env_file_encoding = 'utf-8'  # Garantir que a codificação esteja correta
        case_sensitive = True  # As variáveis de ambiente são sensíveis a maiúsculas e minúsculas
        extra = 'allow'  # Permite variáveis extras não definidas no modelo

    @property
    def DATABASE_URL(self) -> str:
         return f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

def get_database_url() -> str:
    settings = Settings()  # Criação da instância das configurações
    print("DATABASE_URL:", settings.DATABASE_URL)  # Verificando se a URL está correta
    return settings.DATABASE_URL


# Instanciação das configurações
settings: Settings = Settings()  # Criação da instância para ser utilizada em outros arquivos