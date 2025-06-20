from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database.session import get_async_session
from app.api.models.produto_tarefa import Produto_Tarefa
from app.Schema.produto_tarefa_schema import (
    Produto_TaferaCreate,
    Produto_TaferaRead,
    Produto_TaferaUpdate,
)


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

@router.post("/produto_tarefa", response_model=Produto_TaferaRead)
async def criar_produto_tarefa(p_data: Produto_TaferaCreate, db: AsyncSession = Depends(get_async_session)):
    novo = Produto_Tarefa(
        produto_taf_nome=p_data.produto_taf_nome,
        data_execucao=p_data.data_execucao
    )
    db.add(novo)
    await db.commit()
    await db.refresh(novo)
    await manager.broadcast("update")
    return novo

@router.get("/produto_tarefa", response_model=List[Produto_TaferaRead])
async def listar(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Produto_Tarefa))
    return result.scalars().all()

@router.get("/produto_tarefa/{p_id}", response_model=Produto_TaferaRead)
async def buscar(p_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Produto_Tarefa).where(Produto_Tarefa.id == p_id))
    produto = result.scalars().first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto tarefa não encontrado")
    return produto

@router.put("/produto_tarefa/{p_id}", response_model=Produto_TaferaRead)
async def atualizar(p_id: int, p_data: Produto_TaferaUpdate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Produto_Tarefa).where(Produto_Tarefa.id == p_id))
    produto = result.scalars().first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto tarefa não encontrado")

    produto.produto_taf_nome = p_data.produto_taf_nome
    produto.data_execucao = p_data.data_execucao

    await db.commit()
    await db.refresh(produto)
    await manager.broadcast("update")
    return produto

@router.delete("/produto_tarefa/{p_id}", status_code=204)
async def deletar(p_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Produto_Tarefa).where(Produto_Tarefa.id == p_id))
    produto = result.scalars().first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto tarefa não encontrado")
    await db.delete(produto)
    await db.commit()
    await manager.broadcast("update")
    return

@router.websocket("/ws/produto_tarefa")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
