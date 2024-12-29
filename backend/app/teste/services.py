#app/teste/services.py
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.teste import Teste

class UsuarioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, curso: Teste) -> Teste:
        self.db.add(curso)
        await self.db.commit()
        await self.db.refresh(curso)
        return curso

    async def get_all(self) -> List[Teste]:
        result = await self.db.execute(select(Teste))
        cursos = result.scalars().all()
        return cursos

    async def get_by_id(self, curso_id: int) -> Teste:
        result = await self.db.execute(select(Teste).filter(Teste.id == curso_id))
        curso = result.scalars().first()
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso with id {curso_id} not found"
            )
        return curso

    async def update(self, curso_id: int, curso_data: Teste) -> Teste:
        curso = await self.get_by_id(curso_id)
        if curso:
            curso.titulo = curso_data.titulo
            curso.aulas = curso_data.aulas
            curso.horas = curso_data.horas
            await self.db.commit()
            await self.db.refresh(curso)
            return curso
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso with id {curso_id} not found"
        )

    async def delete(self, curso_id: int) -> bool:
        curso = await self.get_by_id(curso_id)
        if curso:
            await self.db.delete(curso)
            await self.db.commit()
            return True
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso with id {curso_id} not found"
        )
