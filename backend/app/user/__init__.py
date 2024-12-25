from fastapi import APIRouter

# Criar um roteador para o módulo 'cliente'
users_router = APIRouter()

# Importar as rotas
from . import routes