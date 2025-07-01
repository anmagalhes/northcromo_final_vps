import asyncio
from fastapi import APIRouter, HTTPException, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from typing import List, Optional

from app.database.session import get_async_session
from app.api.models.cliente import Cliente as ClienteModel
from app.Schema.cliente_schema import (
    ClienteCreate,
    ClienteUpdate,
    ClienteRead,
    PaginatedClientes
)

router = APIRouter()


# Gerenciador de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)


cliente_ws_manager = ConnectionManager()  # Nome consistente

# ✅ Criar cliente
@router.post("/clientes", response_model=ClienteRead)
async def criar_cliente(
    cliente_data: ClienteCreate, db: AsyncSession = Depends(get_async_session)
):
    try:
        cliente = ClienteModel(**cliente_data.dict())
        db.add(cliente)
        await db.commit()
        await db.refresh(cliente)

        await cliente_ws_manager.broadcast("update")  # Notifica via WS

        return cliente
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar cliente: {str(e)}")


# ✅ Listar clientes com paginação e busca
@router.get("/clientes", response_model=PaginatedClientes)
async def listar_clientes(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1),
    search: Optional[str] = Query(None, description="Filtrar por nome ou documento"),
    db: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(ClienteModel)
        count_query = select(func.count(ClienteModel.id))

        if search:
            like_pattern = f"%{search.lower()}%"
            query = query.where(
                func.lower(ClienteModel.nome_cliente).like(like_pattern)
                | func.lower(ClienteModel.doc_cliente).like(like_pattern)
            )
            count_query = count_query.where(
                func.lower(ClienteModel.nome_cliente).like(like_pattern)
                | func.lower(ClienteModel.doc_cliente).like(like_pattern)
            )

        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        query = query.offset((page - 1) * limit).limit(limit)
        result = await db.execute(query)
        clientes = result.scalars().all()

        return {
            "data": clientes,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total // limit) + int(total % limit > 0),
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")


# ✅ Obter cliente por ID
@router.get("/clientes/{cliente_id}", response_model=ClienteRead)
async def obter_cliente(cliente_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(
            select(ClienteModel).where(ClienteModel.id == cliente_id)
        )
        cliente = result.scalars().first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return cliente
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar cliente: {str(e)}")


# ✅ Atualizar cliente
@router.put("/clientes/{cliente_id}", response_model=ClienteRead)
async def atualizar_cliente(
    cliente_id: int,
    cliente_data: ClienteUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        result = await db.execute(select(ClienteModel).where(ClienteModel.id == cliente_id))
        cliente = result.scalars().first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        for field, value in cliente_data.dict(exclude_unset=True).items():
            setattr(cliente, field, value)

        await db.commit()
        await db.refresh(cliente)

        await cliente_ws_manager.broadcast("update")  # Notifica via WS

        return cliente
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")


# ✅ Deletar cliente
@router.delete("/clientes/{cliente_id}", status_code=204)
async def deletar_cliente(cliente_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(ClienteModel).where(ClienteModel.id == cliente_id))
        cliente = result.scalars().first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        await db.delete(cliente)
        await db.commit()

        await cliente_ws_manager.broadcast("update")  # Notifica via WS

        return
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar cliente: {str(e)}")


# ✅ WebSocket para notificações de atualização
@router.websocket("/ws/cliente")
async def websocket_cliente(websocket: WebSocket):
    await cliente_ws_manager.connect(websocket)
    print(f"✅ Cliente WS conectado: {websocket.client}")
    try:
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=60)
            except asyncio.TimeoutError:
                await websocket.send_text("ping")  # Mantém a conexão ativa
    except WebSocketDisconnect:
        cliente_ws_manager.disconnect(websocket)
        print(f"🔌 Cliente WS desconectado: {websocket.client}")
