# checklist_recebimento/__init__.py
from fastapi import APIRouter

# Criar um roteador para o módulo 'cliente'
checklist_recebimento_router = APIRouter()

# Importar as rotas
from . import routes

