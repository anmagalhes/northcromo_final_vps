from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.database.session import get_async_session
from app.api.models.checklist_recebimento import ChecklistRecebimento as ChecklistRecebimentoModel
from app.api.models.recebimento import Recebimento
from app.Schema.checklist_recebimento_schema import ChecklistRecebimentoCreate, ChecklistRecebimentoRead

router = APIRouter()

@router.post("/checklist/", response_model=ChecklistRecebimentoRead)
async def criar_ou_atualizar_checklist(
    checklist_data: ChecklistRecebimentoCreate,
    db: AsyncSession = Depends(get_async_session),
):
    result_recebimento = await db.execute(select(Recebimento).filter(Recebimento.id == checklist_data.recebimento_id))
    recebimento = result_recebimento.scalars().first()
    if not recebimento:
        raise HTTPException(status_code=404, detail="Recebimento não encontrado")

    result_checklist = await db.execute(
        select(ChecklistRecebimentoModel).filter(
            ChecklistRecebimentoModel.recebimento_id == checklist_data.recebimento_id
        )
    )
    checklist = result_checklist.scalars().first()

    if not checklist:
        checklist = ChecklistRecebimentoModel(**checklist_data.model_dump())
        db.add(checklist)
    else:
        for field, value in checklist_data.model_dump().items():
            setattr(checklist, field, value)

    try:
        await db.commit()
        await db.refresh(checklist)
        return checklist
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar checklist: {str(e)}")


@router.get("/checklist/{recebimento_id}", response_model=ChecklistRecebimentoRead)
async def obter_checklist(recebimento_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(
        select(ChecklistRecebimentoModel).filter(ChecklistRecebimentoModel.recebimento_id == recebimento_id)
    )
    checklist = result.scalars().first()
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist não encontrado")
    return checklist
