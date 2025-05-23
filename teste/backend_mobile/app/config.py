import os
from dotenv import load_dotenv

# Exemplo de configuração de credenciais do Google
GOOGLE_CREDENTIALS_PATH = os.getenv(
    "GOOGLE_CREDENTIALS_PATH", "sistemaNortrCromo_googleConsole.json"
)
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

# Configuração do banco de dados
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./test.db"
)  # Se DATABASE_URL não estiver definido no .env, usará sqlite por padrão.


# Caso você precise acessar essas configurações em outras partes da aplicação
def get_google_credentials_path():
    return GOOGLE_CREDENTIALS_PATH


def get_upload_dir():
    return UPLOAD_DIR


def get_database_url():
    return DATABASE_URL
