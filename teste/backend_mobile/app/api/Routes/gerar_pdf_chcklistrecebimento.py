import asyncio
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from concurrent.futures import ThreadPoolExecutor
from typing import List

from app.database.session import get_async_session
from app.api.models.checklist_recebimento import ChecklistRecebimento as ChecklistModel
from app.Schema.checklist_recebimento_schema import ChecklistRecebimentoRead

from app.utils.drive_checklist_rec_docs_service import gerar_pdf_dinamico  # Função usada no executor

router = APIRouter()

executor = ThreadPoolExecutor(max_workers=2)


# Gerenciador de conexões WebSocket
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


def gerar_pdf_sync(id_recebimento, dados):
    return gerar_pdf_dinamico(id_recebimento, dados)


@router.get("/checklisttestes/{recebimento_id}", response_model=ChecklistRecebimentoRead)
async def get_checklist(recebimento_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(ChecklistModel).filter(ChecklistModel.recebimento_id == recebimento_id))
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
                loop = asyncio.get_event_loop()
                resultado = await loop.run_in_executor(
                    executor, gerar_pdf_sync, recebimento_id, dados
                )
                checklist.link_pdf = resultado["pdf_url"]

                db.add(checklist)
                await db.commit()
                await db.refresh(checklist)

                await manager.broadcast("update")  # Notifica clientes se necessário

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erro ao gerar PDF: {str(e)}")

        return checklist

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar checklist: {str(e)}")


@router.websocket("/ws/checklist")
async def websocket_checklist(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
