from fastapi import APIRouter
from app.teste.endpoints import Curso

api_router = APIRouter()

# Corrigindo o erro de digitação e a string do prefixo
api_router.include_router(Curso.router, prefix='/cursos', tags=['Curso'])
