from fastapi import APIRouter

# Criar um roteador para o módulo 'cliente'
componente_router = APIRouter()

# Importar as rotas
from . import routes
