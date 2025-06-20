#app/api/Routes/funcao.py
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from app.database.session import get_async_session
from app.api.models.funcao import Funcao
from app.Schema.funcao_schema import FuncaoCreate, FuncaoRead

router = APIRouter()

# Gerenciador de WebSocket para notificar clientes
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

import traceback

@router.post("/funcoes", response_model=FuncaoRead)
async def criar_funcao(funcao_data: FuncaoCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        funcao = Funcao(
            funcao_nome=funcao_data.funcao_nome,
            data_cadastro=funcao_data.data_cadastro
        )
        db.add(funcao)
        await db.commit()
        await db.refresh(funcao)

        await manager.broadcast("update")

        return funcao
    except SQLAlchemyError as e:
        await db.rollback()
        print(traceback.format_exc())  # imprime no console o erro completo
        raise HTTPException(status_code=500, detail=f"Erro ao criar função: {str(e)}")


@router.get("/funcoes", response_model=List[FuncaoRead])
async def listar_funcoes(db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Funcao))
        funcoes = result.scalars().all()
        return funcoes
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar funções: {str(e)}")


@router.get("/funcoes/{funcao_id}", response_model=FuncaoRead)
async def obter_funcao(funcao_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Funcao).where(Funcao.id == funcao_id))
        funcao = result.scalars().first()
        if not funcao:
            raise HTTPException(status_code=404, detail="Função não encontrada")
        return funcao
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar função: {str(e)}")


@router.put("/funcoes/{funcao_id}", response_model=FuncaoRead)
async def atualizar_funcao(funcao_id: int, funcao_data: FuncaoCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Funcao).where(Funcao.id == funcao_id))
        funcao = result.scalars().first()
        if not funcao:
            raise HTTPException(status_code=404, detail="Função não encontrada")

        funcao.funcao_nome = funcao_data.funcao_nome
        await db.commit()
        await db.refresh(funcao)

        await manager.broadcast("update")

        return funcao
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar função: {str(e)}")


@router.delete("/funcoes/{funcao_id}", status_code=204)
async def deletar_funcao(funcao_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Funcao).where(Funcao.id == funcao_id))
        funcao = result.scalars().first()
        if not funcao:
            raise HTTPException(status_code=404, detail="Função não encontrada")

        await db.delete(funcao)
        await db.commit()

        await manager.broadcast("update")
        return
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar função: {str(e)}")


@router.websocket("/ws/funcoes")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # mantém conexão viva
    except WebSocketDisconnect:
        manager.disconnect(websocket)
