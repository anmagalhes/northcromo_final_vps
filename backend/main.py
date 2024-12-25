import sys
import os

# Adiciona o diretório 'app' ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from fastapi import FastAPI
from app.core.config import settings

# ROUTES
from app.teste import teste_router

# instância
app = FastAPI(title='Sistema Controle interno - Northcromo')

# Incluindo o roteador com prefixo e tags
app.include_router(teste_router, prefix='/api/curso', tags=["curso"])

# Variável 'application' que o Gunicorn espera (opcional, apenas para Gunicorn)
#application = app

if __name__ == "__main__":
    import uvicorn

    # Executa o servidor com a configuração correta
    uvicorn.run("main:app", host="0.0.0.0", port=8000, 
                log_level="info", reload=True)

