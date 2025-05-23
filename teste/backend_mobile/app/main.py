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
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI, Request  # <--- Adiciona o Request aqui
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File, APIRouter
from typing import List


from app.core.database import engine
from app.api.models import Base  # ou onde estiver seu Base declarativo

# Incluindo diretórios no sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

# Importando as rotas de recebimento
from app.api.Routes.recebimento import router as recebimento_router
from app.api.Routes.file_upload import router as file_upload_router
from app.api.Routes.ordem_nova import router as  ordemnova_router
from app.api.Routes.gerar_pdf_chcklistrecebimento import router as gerar_pdf_router

# Definição do FastAPI
app = FastAPI()

# Adicionar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Permite todas as origens (em produção, defina origens específicas)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)


# Middleware para logar o corpo da requisição
@app.middleware("http")
async def log_request(request: Request, call_next):
    body = await request.body()
    print(
        f"Corpo da solicitação: {body[:500]}"
    )  # Limite de 500 bytes para evitar prints enormes
    response = await call_next(request)
    return response


# Inclui as rotas de upload de arquivos
app.include_router(file_upload_router)
app.include_router(recebimento_router)
app.include_router(ordemnova_router)
app.include_router(gerar_pdf_router)

@app.on_event("startup")
async def startup_event():
    print("Rotas carregadas:")
    for route in app.routes:
        print(route.path)

