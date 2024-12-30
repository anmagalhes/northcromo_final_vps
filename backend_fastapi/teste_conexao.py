# verificar_url.py
from app.core.config import Settings

# Criando uma instância das configurações
settings = Settings()

# Imprimindo a URL do banco de dados
print("DATABASE_URL:", settings.DATABASE_URL)
