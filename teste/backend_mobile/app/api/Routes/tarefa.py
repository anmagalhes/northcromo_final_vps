import asyncio
from fastapi import APIRouter, HTTPException, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import selectinload

from app.database.session import get_async_session
from app.api.models.tarefa import Tarefa
from app.api.models.checklist_recebimento import ChecklistRecebimento
from app.api.models.tarefa import Tarefa as TarefaModel
from app.Schema.tarefa_schema import (
    TarefaCreate,
    TarefaRead,
    TarefaUpdate,
    PaginatedTarefas,
)

from app.api.models.recebimento import Recebimento
from app.api.models.enums import StatusTarefaEnum
from app.api.models.checklist_recebimento import ChecklistRecebimento

router = APIRouter()

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
                # Se algum erro acontecer, desconecta o client
                self.disconnect(connection)

manager = ConnectionManager()

@router.post("/tarefas", response_model=TarefaRead)
async def criar_tarefa(tarefa_data: TarefaCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        tarefa = TarefaModel(
            recebimento_id=tarefa_data.recebimento_id,
            data_rec_ordem=tarefa_data.data_rec_ordem,
            qtde_servico=tarefa_data.qtde_servico,
            id_servico=tarefa_data.id_servico,
            id_servico2=tarefa_data.id_servico2,
            id_operacao=tarefa_data.id_operacao,
            desc_servico_produto=tarefa_data.desc_servico_produto,
            obs=tarefa_data.obs,
            status=tarefa_data.status or StatusTarefaEnum.PENDENTE,
            referencia_produto=tarefa_data.referencia_produto,
            nota_interna=tarefa_data.nota_interna,
            data_checklist_ordem=tarefa_data.data_checklist_ordem,
        )
        db.add(tarefa)
        await db.commit()
        await db.refresh(tarefa)

        await manager.broadcast("update")  # Notifica todos os clients websocket

        return tarefa
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar tarefa: {str(e)}")

@router.get("/tarefas", response_model=PaginatedTarefas)
async def listar_tarefas(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        # Consulta para incluir o relacionamento com nota fiscal
        query = select(TarefaModel).options(
                selectinload(TarefaModel.recebimento).selectinload(Recebimento.cliente),
                selectinload(Tarefa.checklist).selectinload(ChecklistRecebimento.recebimento).selectinload(Recebimento.cliente)
            )

        count_query = select(func.count(TarefaModel.id))

         # Filtro de status, se presente
        if status:
            query = query.where(TarefaModel.status == status)
            count_query = count_query.where(TarefaModel.status == status)

        # Executa a contagem total de tarefas
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

       # Aplica a paginação (offset + limit)
        query = query.offset((page - 1) * limit).limit(limit)

        # Executa a consulta para obter as tarefas
        result = await db.execute(query)
        tarefas = result.scalars().all()

        return {
            "data": tarefas,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total // limit) + int(total % limit > 0)
        }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar tarefas: {str(e)}")

@router.get("/tarefas/{tarefa_id}", response_model=TarefaRead)
async def obter_tarefa(tarefa_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(
            select(TarefaModel)
            .options(
                selectinload(TarefaModel.recebimento),
                selectinload(TarefaModel.checklist)
            )
            .where(TarefaModel.id == tarefa_id)
        )
        tarefa = result.scalars().first()
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        return tarefa
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar tarefa: {str(e)}")

@router.put("/tarefas/{tarefa_id}", response_model=TarefaRead)
async def atualizar_tarefa(
    tarefa_id: int,
    tarefa_data: TarefaUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        result = await db.execute(select(TarefaModel).where(TarefaModel.id == tarefa_id))
        tarefa = result.scalars().first()
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")

        for field, value in tarefa_data.dict(exclude_unset=True).items():
            setattr(tarefa, field, value)

        await db.commit()
        await db.refresh(tarefa)

        await manager.broadcast("update")

        return tarefa
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar tarefa: {str(e)}")

@router.delete("/tarefas/{tarefa_id}", status_code=204)
async def deletar_tarefa(tarefa_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(TarefaModel).where(TarefaModel.id == tarefa_id))
        tarefa = result.scalars().first()
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")

        await db.delete(tarefa)
        await db.commit()

        await manager.broadcast("update")

        return
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar tarefa: {str(e)}")
@router.websocket("/ws/tarefa")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print(f"Conexão WS aberta: {websocket.client}")
    try:
        while True:
            # Aqui você pode enviar ping, ou só esperar com timeout
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=60)
            except asyncio.TimeoutError:
                # opcional: enviar ping para manter vivo
                await websocket.send_text("ping")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Conexão WS fechada: {websocket.client}")
