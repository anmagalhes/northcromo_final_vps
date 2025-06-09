#app/api/Routes/defeito.py
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from app.database.session import get_async_session
from app.api.models.defeito import Defeito
from app.Schema.defeito_schema import DefeitoCreate, DefeitoRead
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


@router.post("/defeito", response_model=DefeitoRead)
async def criar_defeito(defeito_data: DefeitoCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        defeito = Defeito(
            def_nome=defeito_data.def_nome,
            data=defeito_data.data,
            componente_id=defeito_data.componente_id,
        )
        db.add(defeito)
        await db.commit()
        await db.refresh(defeito)

        # Carrega o relacionamento explicitamente após o commit
        await db.refresh(defeito, attribute_names=["componente"])

        await manager.broadcast("update")  # Notifica clientes via WebSocket

        return DefeitoRead(
            id=defeito.id,
            def_nome=defeito.def_nome,
            data=defeito.data,
            componente_id=defeito.componente_id,
            componente_nome=defeito.componente.componente_nome if defeito.componente else None,
        )

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar defeito: {str(e)}")


@router.get("/defeito", response_model=List[DefeitoRead])
async def listar_defeitos(db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Defeito).options(selectinload(Defeito.componente)))
        defeitos = result.scalars().all()

        response = [
            DefeitoRead(
                id=d.id,
                def_nome=d.def_nome,
                data=d.data,
                componente_id=d.componente_id,
                componente_nome=d.componente.componente_nome if d.componente else None,
            )
            for d in defeitos
        ]


        await manager.broadcast("update")  # Notifica clientes via WebSocket

        return response
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar defeitos: {str(e)}")


@router.get("/defeito/{defeito_id}", response_model=DefeitoRead)
async def buscar_defeito(defeito_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(
            select(Defeito).where(Defeito.id == defeito_id).options(selectinload(Defeito.componente))
        )
        defeito = result.scalars().first()

        if not defeito:
            raise HTTPException(status_code=404, detail="Defeito não encontrado")

        return DefeitoRead(
            id=defeito.id,
            def_nome=defeito.def_nome,
            data=defeito.data,
            componente_id=defeito.componente_id,
            componente_nome=defeito.componente.nome if defeito.componente else None,
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar defeito: {str(e)}")

@router.put("/defeito/{defeito_id}", response_model=DefeitoRead)
async def atualizar_defeito(defeito_id: int, defeito_data: DefeitoCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(
            select(Defeito).where(Defeito.id == defeito_id).options(selectinload(Defeito.componente))
        )
        defeito = result.scalars().first()

        if not defeito:
            raise HTTPException(status_code=404, detail="Defeito não encontrado")

        defeito.def_nome = defeito_data.def_nome
        defeito.data = defeito_data.data
        defeito.componente_id = defeito_data.componente_id

        await db.commit()
        await db.refresh(defeito)
        await db.refresh(defeito, attribute_names=["componente"])

        await manager.broadcast("update")

        return DefeitoRead(
            id=defeito.id,
            def_nome=defeito.def_nome,
            data=defeito.data,
            componente_id=defeito.componente_id,
            componente_nome=defeito.componente.nome if defeito.componente else None,
        )

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar defeito: {str(e)}")

@router.delete("/defeito/{defeito_id}", status_code=204)
async def deletar_defeito(defeito_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Defeito).where(Defeito.id == defeito_id))
        defeito = result.scalars().first()

        if not defeito:
            raise HTTPException(status_code=404, detail="Defeito não encontrado")

        await db.delete(defeito)
        await db.commit()

        await manager.broadcast("update")  # Notifica clientes

        return

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar defeito: {str(e)}")


@router.websocket("/ws/defeito")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # mantém conexão ativa
    except WebSocketDisconnect:
        manager.disconnect(websocket)
