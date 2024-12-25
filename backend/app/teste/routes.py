# app/teste/routes.py
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.teste import Teste
from app.teste.services import CursoService
from core.desp import get_session

# BYpass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

# Corrigindo o nome do método `inherit_cache` (ao invés de `inrerit_cache`)
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
# Fim BYpass

api_router = APIRouter()

# POST CURSO
@api_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Teste)
async def post_curso(curso: Teste, db: AsyncSession = Depends(get_session)):
    service = CursoService(db)
    return await service.create(curso)

# GET CURSOS
@api_router.get('/', response_model=List[Teste])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    service = CursoService(db)
    return await service.get_all()

# GET CURSO POR ID
@api_router.get('/{curso_id}', response_model=Teste, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    service = CursoService(db)
    curso = await service.get_by_id(curso_id)
    if not curso:
        raise HTTPException(
            detail='Curso não encontrado',
            status_code=status.HTTP_404_NOT_FOUND
        )
    return curso

# PUT CURSO
@api_router.put('/{curso_id}', status_code=status.HTTP_202_ACCEPTED, response_model=Teste)
async def put_curso(curso_id: int, curso: Teste, db: AsyncSession = Depends(get_session)):
    service = CursoService(db)
    updated_curso = await service.update(curso_id, curso)
    if not updated_curso:
        raise HTTPException(
            detail='Curso não encontrado',
            status_code=status.HTTP_404_NOT_FOUND
        )
    return updated_curso

# DELETE CURSO
@api_router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    service = CursoService(db)
    deleted = await service.delete(curso_id)
    if not deleted:
        raise HTTPException(
            detail='Curso não encontrado',
            status_code=status.HTTP_404_NOT_FOUND
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Sem conteúdo na resposta
