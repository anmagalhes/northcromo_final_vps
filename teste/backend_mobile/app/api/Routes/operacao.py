from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.database.session import get_async_session
from app.api.models.operacao import Operacao
from app.Schema.operacao_schema import OperacaoCreate, OperacaoRead
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


@router.post("/operacao", response_model=OperacaoRead)
async def criar_operacao(
    operacao_data: OperacaoCreate, db: AsyncSession = Depends(get_async_session)
):
    try:
        operacao = Operacao(
            op_grupo_processo=operacao_data.op_grupo_processo,
            op_nome=operacao_data.op_nome
        )
        db.add(operacao)
        await db.commit()
        await db.refresh(operacao)

        await manager.broadcast("update")  # Notifica clientes via WebSocket

        return operacao

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar operação: {str(e)}")


@router.get("/operacao", response_model=List[OperacaoRead])
async def listar_operacoes(db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Operacao))
        operacoes = result.scalars().all()
        return operacoes
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar operações: {str(e)}")


@router.get("/operacao/{operacao_id}", response_model=OperacaoRead)
async def buscar_operacao(operacao_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Operacao).where(Operacao.id == operacao_id))
        operacao = result.scalars().first()

        if not operacao:
            raise HTTPException(status_code=404, detail="Operação não encontrada")

        return operacao
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar operação: {str(e)}")


@router.put("/operacao/{operacao_id}", response_model=OperacaoRead)
async def atualizar_operacao(
    operacao_id: int, operacao_data: OperacaoCreate, db: AsyncSession = Depends(get_async_session)
):
    try:
        result = await db.execute(select(Operacao).where(Operacao.id == operacao_id))
        operacao = result.scalars().first()

        if not operacao:
            raise HTTPException(status_code=404, detail="Operação não encontrada")

        operacao.op_grupo_processo = operacao_data.op_grupo_processo
        operacao.op_nome = operacao_data.op_nome

        await db.commit()
        await db.refresh(operacao)

        await manager.broadcast("update")  # Notifica clientes

        return operacao

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar operação: {str(e)}")


@router.delete("/operacao/{operacao_id}", status_code=204)
async def deletar_operacao(operacao_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Operacao).where(Operacao.id == operacao_id))
        operacao = result.scalars().first()

        if not operacao:
            raise HTTPException(status_code=404, detail="Operação não encontrada")

        await db.delete(operacao)
        await db.commit()

        await manager.broadcast("update")  # Notifica clientes

        return

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar operação: {str(e)}")


@router.websocket("/ws/operacoes")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # mantém conexão ativa
            # opcionalmente processe 'data' aqui ou ignore
    except WebSocketDisconnect:
        manager.disconnect(websocket)
