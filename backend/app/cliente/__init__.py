# app/cliente/__init__.py
from fastapi import APIRouter

# Criar um roteador para o módulo 'cliente'
cliente_router = APIRouter()

# Importar as rotas
from . import routes
