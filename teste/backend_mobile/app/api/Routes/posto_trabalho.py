#app/api/Routes/posto_trabalho.py
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from sqlalchemy.orm.attributes import flag_modified


from app.database.session import get_async_session
from app.api.models.posto_trabalho import Posto_Trabalho
from app.Schema.posto_trabalho_schema import Posto_TrabalhoCreate, Posto_TrabalhoRead, Posto_TrabalhoUpdate


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

@router.post("/posto_trabalho", response_model=Posto_TrabalhoRead)
async def criar_posto_trabalho(
    posto_data: Posto_TrabalhoCreate, db: AsyncSession = Depends(get_async_session)
):
    try:
        posto = Posto_Trabalho(
            posto_trabalho_nome=posto_data.posto_trabalho_nome,
            data_execucao=posto_data.data_execucao,
        )
        db.add(posto)
        await db.commit()
        await db.refresh(posto)

        await manager.broadcast("update")  # Notifica clientes via WebSocket

        return posto

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar posto de trabalho: {str(e)}")


@router.get("/posto_trabalho", response_model=List[Posto_TrabalhoRead])
async def listar_postos_trabalho(db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Posto_Trabalho))
        postos = result.scalars().all()
        return postos
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar postos de trabalho: {str(e)}")


@router.get("/posto_trabalho/{posto_id}", response_model=Posto_TrabalhoRead)
async def buscar_posto_trabalho(posto_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Posto_Trabalho).where(Posto_Trabalho.id == posto_id))
        posto = result.scalars().first()

        if not posto:
            raise HTTPException(status_code=404, detail="Posto de trabalho não encontrado")

        return posto
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar posto de trabalho: {str(e)}")


@router.put("/posto_trabalho/{posto_id}", response_model=Posto_TrabalhoRead)
async def atualizar_posto_trabalho(
    posto_id: int,
    posto_data: Posto_TrabalhoUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        result = await db.execute(select(Posto_Trabalho).where(Posto_Trabalho.id == posto_id))
        posto = result.scalars().first()

        if not posto:
            raise HTTPException(status_code=404, detail="Posto de trabalho não encontrado")

        posto.posto_trabalho_nome = posto_data.posto_trabalho_nome
        posto.data_execucao = posto_data.data_execucao

        await db.commit()
        await db.refresh(posto)

        await manager.broadcast("update")  # Notifica clientes

        return posto

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar posto de trabalho: {str(e)}")


@router.delete("/posto_trabalho/{posto_id}", status_code=204)
async def deletar_posto_trabalho(posto_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Posto_Trabalho).where(Posto_Trabalho.id == posto_id))
        posto = result.scalars().first()

        if not posto:
            raise HTTPException(status_code=404, detail="Posto de trabalho não encontrado")

        await db.delete(posto)
        await db.commit()

        await manager.broadcast("update")  # Notifica clientes

        return

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar posto de trabalho: {str(e)}")


@router.websocket("/ws/posto_trabalho")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # mantém conexão ativa
    except WebSocketDisconnect:
        manager.disconnect(websocket)
