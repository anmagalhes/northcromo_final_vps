import os
from dotenv import load_dotenv
import base64

load_dotenv()  # Carrega variáveis do .env

# Caminho onde o arquivo JSON das credenciais será criado
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "sistemaNortrCromo_googleConsole.json")

# Pega a string base64 do arquivo JSON (vinda do .env)
google_credentials_b64 = os.getenv("GOOGLE_CREDENTIALS_B64")

# Se a variável existe, cria o arquivo JSON no disco para o Google SDK usar
if google_credentials_b64:
    with open(GOOGLE_CREDENTIALS_PATH, "wb") as f:
        f.write(base64.b64decode(google_credentials_b64))

# Define a variável de ambiente para o SDK do Google encontrar o arquivo JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH


# Continua com as outras configurações do seu sistema
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


def get_google_credentials_path():
    return GOOGLE_CREDENTIALS_PATH


def get_upload_dir():
    return UPLOAD_DIR


def get_database_url():
    return DATABASE_URL
