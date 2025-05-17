from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

class Settings:
    # Carregar a variável DATABASE_URL e fornecer um valor padrão se não for encontrada
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Padrão é usar sqlite se não houver .env

    # Verifique se a variável foi carregada corretamente, caso contrário, levante um erro
    if not DATABASE_URL:
        raise ValueError("A variável de ambiente DATABASE_URL não foi definida corretamente no arquivo .env")
