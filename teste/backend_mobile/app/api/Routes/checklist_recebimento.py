import asyncio
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.database.session import get_async_session
from app.api.models.checklist_recebimento import ChecklistRecebimento as ChecklistModel
from app.api.models.recebimento import Recebimento
from app.Schema.checklist_recebimento_schema import (
    ChecklistRecebimentoCreate,
    ChecklistRecebimentoRead,
    ChecklistRecebimentoUpdate,
)

from fastapi import Query
from sqlalchemy import func

from app.utils.drive_checklist_rec_docs_service import gerar_pdf_dinamico  # Função usada no executor
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import selectinload

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=2)


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

@router.post("/checklist", response_model=ChecklistRecebimentoRead)
async def criar_checklist(
    checklist_data: ChecklistRecebimentoCreate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        result = await db.execute(select(Recebimento).where(Recebimento.id == checklist_data.recebimento_id))
        recebimento = result.scalars().first()
        if not recebimento:
            raise HTTPException(status_code=404, detail="Recebimento não encontrado")

        checklist = ChecklistModel(**checklist_data.model_dump())
        db.add(checklist)
        await db.commit()
        await db.refresh(checklist)

        await manager.broadcast("update")
        return checklist

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar checklist: {str(e)}")


@router.get("/checklist")
async def listar_checklists(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1),
    com_pdf: str = Query("all", regex="^(true|false|all)$"),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        #query = select(ChecklistModel)
        query = select(ChecklistModel).options(
            selectinload(ChecklistModel.recebimento),
        )
        # QUANDO TEM RELACIONAMENTOS
       # query = select(ChecklistModel).options(
       #     selectinload(ChecklistModel.recebimento)
       #         .selectinload(Recebimento.cliente),
       # )

        count_query = select(func.count(ChecklistModel.id))

        if com_pdf == "true":
            query = query.where(ChecklistModel.link_pdf.isnot(None))
            count_query = count_query.where(ChecklistModel.link_pdf.isnot(None))
        elif com_pdf == "false":
            query = query.where(ChecklistModel.link_pdf.is_(None))
            count_query = count_query.where(ChecklistModel.link_pdf.is_(None))

        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        query = query.offset((page - 1) * limit).limit(limit)
        result = await db.execute(query)
        checklists = result.scalars().all()

        return {
            "data": [ChecklistRecebimentoRead.model_validate(c, from_attributes=True) for c in checklists],
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total // limit) + (1 if total % limit else 0)
        }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar checklists: {str(e)}")


import traceback  # <-- adicione isso no topo se não tiver

def gerar_pdf_sync(id_recebimento, dados):
    return gerar_pdf_dinamico(id_recebimento, dados)

async def gerar_pdf_async(recebimento_id, dados):
    loop = asyncio.get_running_loop()
    # roda gerar_pdf_sync numa thread paralela para não bloquear o event loop
    resultado = await loop.run_in_executor(executor, gerar_pdf_sync, recebimento_id, dados)
    return resultado

@router.get("/checklist/{recebimento_id}", response_model=ChecklistRecebimentoRead)
async def obter_checklist(recebimento_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(
            #select(ChecklistModel).where(ChecklistModel.recebimento_id == recebimento_id)
            select(ChecklistModel)
            .options(
                selectinload(ChecklistModel.recebimento),
            )
            .where(ChecklistModel.recebimento_id == recebimento_id)
        )
        checklist = result.scalars().first()
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist não encontrado")

        if not checklist.link_pdf:
            dados = {
                "cl": "Cliente Teste",
                "doc.cl": "123.456.789-00",
                "produto": "Produto A",
                "qtd": "20",
                "orcamento": "ORC-9999",
                "o": "1111",
                "a": "5",
                "b": "NF-2025"
            }

            try:
                # Aqui você chama a função async direto, sem precisar do loop ou executor
                resultado = await gerar_pdf_async(recebimento_id, dados)
                print("✅ Resultado do PDF:", resultado)
                checklist.link_pdf = resultado["pdf_url"]

                db.add(checklist)
                await db.commit()
                await db.refresh(checklist)

                await manager.broadcast("update")

            except Exception as e:
                print("🚨 Erro ao gerar PDF:")
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Erro ao gerar PDF: {str(e)}")

        return checklist

    except SQLAlchemyError as e:
        print("🚨 Erro ao buscar no banco:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao buscar checklist: {str(e)}")

    except Exception as e:
        print("🚨 Erro inesperado:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")


@router.put("/checklist/{recebimento_id}", response_model=ChecklistRecebimentoRead)
async def atualizar_checklist(
    recebimento_id: int,
    checklist_data: ChecklistRecebimentoUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        result = await db.execute(
            select(ChecklistModel).where(ChecklistModel.recebimento_id == recebimento_id)
        )
        checklist = result.scalars().first()
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist não encontrado")

        for field, value in checklist_data.model_dump(exclude_unset=True).items():
            setattr(checklist, field, value)

        await db.commit()
        await db.refresh(checklist)

        await manager.broadcast("update")
        return checklist
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar checklist: {str(e)}")


@router.delete("/checklist/{recebimento_id}", status_code=204)
async def deletar_checklist(recebimento_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(
            select(ChecklistModel).where(ChecklistModel.recebimento_id == recebimento_id)
        )
        checklist = result.scalars().first()
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist não encontrado")

        await db.delete(checklist)
        await db.commit()

        await manager.broadcast("update")
        return

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar checklist: {str(e)}")


@router.websocket("/ws/checklist")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantém conexão ativa
    except WebSocketDisconnect:
        manager.disconnect(websocket)
