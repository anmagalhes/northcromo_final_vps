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

from app.utils.google_auth_init import garantir_credenciais_google

# Incluindo diretórios no sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

# Importando as rotas de recebimento
from app.api.Routes.recebimento import router as recebimento_router
from app.api.Routes.file_upload import router as file_upload_router
from app.api.Routes.ordem_nova import router as  ordemnova_router
from app.api.Routes.gerar_pdf_chcklistrecebimento import router as gerar_pdf_router
from app.api.Routes.componente import router as  componente_router
from app.api.Routes.operacao import router as operacao_router
from app.api.Routes.posto_trabalho import router as postotrabalho_router
from app.api.Routes.defeito import router as defeito_router
from app.api.Routes.produto_tarefa import router as tarefa_router
from app.api.Routes.produto import router as produto_router
from app.api.Routes.funcionario import router as funcionario_router
from app.api.Routes.funcao import router as funcao_router
from app.api.Routes.checklist_recebimento import router as checklist_recebimento_router
from app.api.Routes.tarefa import router as novas_tarefas_router
from app.api.Routes.cliente import router as cliente_router


# Definição do FastAPI
app = FastAPI()
#application = app para o deploy

title="Northcromo API",
description="Documentação da API de Recebimento, Componentes e Checklists",
version="1.0.0"

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
app.include_router(file_upload_router, prefix="/api", tags=["Recebimento"])
app.include_router(recebimento_router, prefix="/api", tags=["Recebimento"])
app.include_router(ordemnova_router, prefix="/api", tags=["Recebimento"])
app.include_router(gerar_pdf_router, prefix="/api", tags=["Checklist Recebimento"])
app.include_router(componente_router, prefix="/api", tags=["Cadastro"])
app.include_router(operacao_router, prefix="/api", tags=["Cadastro"])
app.include_router(postotrabalho_router, prefix="/api", tags=["Cadastro"])
app.include_router(defeito_router, prefix="/api", tags=["Cadastro"])
app.include_router(tarefa_router, prefix="/api", tags=["Cadastro"])
app.include_router(produto_router, prefix="/api", tags=["Cadastro"])
app.include_router(funcionario_router, prefix="/api", tags=["Cadastro"])
app.include_router(funcao_router, prefix="/api", tags=["Cadastro"])
app.include_router(checklist_recebimento_router, prefix="/api", tags=["Checklist Recebimento"])
app.include_router(novas_tarefas_router, prefix="/api/novas-tarefas", tags=["novas_tarefas"])
app.include_router(cliente_router, prefix="/api", tags=["Cadastro"])


@app.on_event("startup")
async def startup_event():
    print("Rotas carregadas:")
    for route in app.routes:
        print(route.path)
    garantir_credenciais_google()


