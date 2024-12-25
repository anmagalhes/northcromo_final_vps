#app/teste/endpoints/curso.py
from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.teste import Teste
from core.desp import get_session

# BYpass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectofScalar

# Corrigindo o nome do método `inherit_cache` (ao invés de `inrerit_cache`)
SelectofScalar.inherit_cache = True
Select.inherit_cache = True
# Fim BYpass

router = APIRouter()

# POST CURSO
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Teste)
async def post_curso(curso: Teste, db: AsyncSession = Depends(get_session)):
    novo_curso = Teste(
        titulo=curso.titulo,
        aulas=curso.aulas,
        horas=curso.horas
    )

    db.add(novo_curso)
    await db.commit()

    return novo_curso

# GET CURSOS
@router.get('/', response_model=List[Teste])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Teste)
        result = await session.execute(query)
        cursos: List[Teste] = result.scalars().all()

        return cursos
    
# GET CURSO POR ID
@router.get('/{curso_id}', response_model=Teste, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Teste).filter(Teste.id == curso_id)
        result = await session.execute(query)
        curso: Teste = result.scalars().one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(
                detail='Curso não encontrado', 
                status_code=status.HTTP_404_NOT_FOUND
            )

# PUT CURSO
@router.put('/{curso_id}', status_code=status.HTTP_202_ACCEPTED, response_model=Teste)
async def put_curso(curso_id: int, curso: Teste, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Teste).filter(Teste.id == curso_id)
        result = await session.execute(query)
        curso_up: Teste = result.scalars().one_or_none()

        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas
            await session.commit()
            return curso_up
        else:
            raise HTTPException(
                detail='Curso não encontrado', 
                status_code=status.HTTP_404_NOT_FOUND
            )

# DELETE CURSO
@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Teste).filter(Teste.id == curso_id)
        result = await session.execute(query)
        cursodel: Teste = result.scalars().one_or_none()

        if cursodel:

            # Remove o curso do banco de dados
            await session.delete(cursodel)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)  # Sem conteúdo na resposta
        else:
            raise HTTPException(
                detail='Curso não encontrado', 
                status_code=status.HTTP_404_NOT_FOUND
            )
