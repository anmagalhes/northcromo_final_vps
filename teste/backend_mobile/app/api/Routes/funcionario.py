# app/api/routes/funcionario.py

from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from app.database.session import get_async_session
from app.api.models.funcionario import Funcionario
from app.Schema.funcionario_schema import FuncionarioCreate, FuncionarioRead, FuncionarioUpdate
from sqlalchemy.orm import selectinload

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


@router.post("/funcionario", response_model=FuncionarioRead)
async def criar_funcionario(funcionario_data: FuncionarioCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        funcionario = Funcionario(**funcionario_data.dict())
        db.add(funcionario)
        await db.commit()
        await db.refresh(funcionario)

        # Se quiser carregar relacionamento, faça aqui (exemplo: usuario)
        await db.refresh(funcionario, attribute_names=["usuario"])

        await manager.broadcast("update")  # Notifica clientes via WebSocket

        return funcionario

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar funcionário: {str(e)}")


@router.get("/funcionario", response_model=List[FuncionarioRead])
async def listar_funcionarios(db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Funcionario).options(selectinload(Funcionario.usuario)))
        funcionarios = result.scalars().all()
        return funcionarios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar funcionários: {str(e)}")


@router.get("/funcionario/{funcionario_id}", response_model=FuncionarioRead)
async def buscar_funcionario(funcionario_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(
            select(Funcionario).where(Funcionario.id == funcionario_id).options(selectinload(Funcionario.usuario))
        )
        funcionario = result.scalars().first()

        if not funcionario:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")

        return funcionario
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar funcionário: {str(e)}")


@router.put("/funcionario/{funcionario_id}", response_model=FuncionarioRead)
async def atualizar_funcionario(funcionario_id: int, funcionario_data: FuncionarioUpdate, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(
            select(Funcionario).where(Funcionario.id == funcionario_id).options(selectinload(Funcionario.usuario))
        )
        funcionario = result.scalars().first()

        if not funcionario:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")

        for key, value in funcionario_data.dict(exclude_unset=True).items():
            setattr(funcionario, key, value)

        await db.commit()
        await db.refresh(funcionario)
        await db.refresh(funcionario, attribute_names=["usuario"])

        await manager.broadcast("update")

        return funcionario

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar funcionário: {str(e)}")


@router.delete("/funcionario/{funcionario_id}", status_code=204)
async def deletar_funcionario(funcionario_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Funcionario).where(Funcionario.id == funcionario_id))
        funcionario = result.scalars().first()

        if not funcionario:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")

        await db.delete(funcionario)
        await db.commit()

        await manager.broadcast("update")  # Notifica clientes

        return

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar funcionário: {str(e)}")


@router.websocket("/ws/funcionario")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # mantém conexão ativa
    except WebSocketDisconnect:
        manager.disconnect(websocket)
