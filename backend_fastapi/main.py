# from app.core.database import init_db
import os
import sys
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

from app.routes import (
    todo,
    user,
    componente,
    postotrabalho,
    recebimento,
    cliente,
    produto,
    funcionario,
    operacao,
)
from app.routes.importacao import (
    cliente_import, 
    componente_import, 
    produto_import,
    operacao_import,

 )

# Definição do FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos os domínios. Para produção, é melhor especificar domínios confiáveis.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)


# PARA O HTML
# Configuração do Jinja2Templates, apontando para a pasta templates
templates = Jinja2Templates(directory="app/templates")

# Registra os controladores de rotas
app.include_router(user.router)
app.include_router(todo.router)
app.include_router(componente.router)
app.include_router(postotrabalho.router)
app.include_router(recebimento.router)
app.include_router(cliente.router)
app.include_router(cliente_import.router)
app.include_router(produto.router)
app.include_router(funcionario.router)
app.include_router(operacao.router)


# Incluindo as rotas de importação arquivo
app.include_router(cliente_import.router)
app.include_router(produto_import.router)
app.include_router(componente_import.router)
app.include_router(operacao_import.router)

# Rota para renderizar o template HTML padrão
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
