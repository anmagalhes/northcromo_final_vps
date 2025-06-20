import os
import base64
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "sistemaNortrCromo_googleConsole.json")
google_credentials_b64 = os.getenv("GOOGLE_CREDENTIALS_B64")

def garantir_credenciais_google():
    if google_credentials_b64 and not os.path.exists(GOOGLE_CREDENTIALS_PATH):
        decoded = base64.b64decode(google_credentials_b64)
        print(f"Gravando credencial Google no arquivo {GOOGLE_CREDENTIALS_PATH}")
        print(f"Conteúdo JSON parcial: {decoded[:200]}")  # mostra só parte para não poluir muito
        with open(GOOGLE_CREDENTIALS_PATH, "wb") as f:
            f.write(decoded)
    else:
        print(f"Arquivo de credencial já existe: {GOOGLE_CREDENTIALS_PATH}")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH
    print(f"Variável GOOGLE_APPLICATION_CREDENTIALS setada para {GOOGLE_CREDENTIALS_PATH}")
