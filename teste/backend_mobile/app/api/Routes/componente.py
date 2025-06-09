#app/api/Routes/componente.py
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import get_async_session
from app.api.models.componente import Componente
from app.Schema.componente_schema import ComponenteSchema, ComponenteCreate, ComponenteRead
from typing import List
import asyncio

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


@router.post("/componente", response_model=ComponenteRead)
async def criar_componente(
    componente_data: ComponenteCreate, db: AsyncSession = Depends(get_async_session)
):
    try:
        componente = Componente(
            componente_nome=componente_data.componente_nome,
            data_recebimento=componente_data.data_recebimento,
        )
        db.add(componente)
        await db.commit()
        await db.refresh(componente)
        await manager.broadcast("update")  # 🔔 Notifica os clientes conectados via WebSocket

        return componente

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar componente: {str(e)}")


@router.get("/componente", response_model=List[ComponenteRead])
async def listar_componentes(db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Componente))
        componentes = result.scalars().all()
        return componentes

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar componentes: {str(e)}")


@router.get("/componente/{componente_id}", response_model=ComponenteRead)
async def buscar_componente(componente_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Componente).where(Componente.id == componente_id))
        componente = result.scalars().first()

        if not componente:
            raise HTTPException(status_code=404, detail="Componente não encontrado")

        return componente

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar componente: {str(e)}")

@router.put("/componente/{componente_id}", response_model=ComponenteRead)
async def atualizar_componente(
    componente_id: int,
    componente_data: ComponenteCreate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        result = await db.execute(select(Componente).where(Componente.id == componente_id))
        componente = result.scalars().first()

        if not componente:
            raise HTTPException(status_code=404, detail="Componente não encontrado")

        componente.componente_nome = componente_data.componente_nome
        componente.data_recebimento = componente_data.data_recebimento

        await db.commit()
        await db.refresh(componente)
        await manager.broadcast("update")  # 🔔 Notifica atualização

        return componente

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar componente: {str(e)}")


@router.delete("/componente/{componente_id}", status_code=204)
async def deletar_componente(
    componente_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        result = await db.execute(select(Componente).where(Componente.id == componente_id))
        componente = result.scalars().first()

        if not componente:
            raise HTTPException(status_code=404, detail="Componente não encontrado")

        await db.delete(componente)
        await db.commit()
        await manager.broadcast("update")

        return

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao excluir componente: {str(e)}")

@router.websocket("/ws/componentes")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # ou await asyncio.sleep(10) para manter conexão
            # processa dados ou mantém conexão aberta
    except WebSocketDisconnect:
        manager.disconnect(websocket)
