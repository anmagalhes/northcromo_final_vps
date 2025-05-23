from dotenv import load_dotenv
import os

load_dotenv()  # carrega as variáveis do arquivo .env

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
ENVIRONMENT = os.getenv("ENVIRONMENT")

print("DB URL:", ASYNC_DATABASE_URL)
print("JWT Secret:", JWT_SECRET)
print("Environment:", ENVIRONMENT)
