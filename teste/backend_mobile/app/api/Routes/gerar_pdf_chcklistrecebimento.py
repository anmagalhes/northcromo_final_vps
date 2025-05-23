import asyncio
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from concurrent.futures import ThreadPoolExecutor

from app.database.session import get_async_session
from app.api.models.checklist_recebimento import ChecklistRecebimento as ChecklistModel
from app.Schema.checklist_recebimento_schema import ChecklistRecebimentoRead  # atenção ao nome da pasta: schemas, não Schema

router = APIRouter()

executor = ThreadPoolExecutor(max_workers=2)

def gerar_pdf_sync(id_recebimento, dados):
    from app.utils.drive_checklist_rec_docs_service import gerar_pdf_dinamico
    return gerar_pdf_dinamico(id_recebimento, dados)

@router.get("/checklist/{recebimento_id}", response_model=ChecklistRecebimentoRead)
async def get_checklist(recebimento_id: int, db: AsyncSession = Depends(get_async_session)):
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

        resultado = await asyncio.get_event_loop().run_in_executor(
            executor, gerar_pdf_sync, recebimento_id, dados
        )
        checklist.link_pdf = resultado["pdf_url"]

        db.add(checklist)
        await db.commit()
        await db.refresh(checklist)

    return checklist
