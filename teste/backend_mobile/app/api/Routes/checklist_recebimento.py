# app/api/routes/checklist_recebimento.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.session import get_db
from app.api.models.checklist_recebimento import ChecklistRecebimento as ChecklistRecebimentoModel
from app.api.models.recebimento import Recebimento
from app.Schema.checklist_recebimento_schema import ChecklistRecebimentoCreate, ChecklistRecebimentoRead

router = APIRouter()

@router.post("/checklist/", response_model=ChecklistRecebimentoRead)
def criar_ou_atualizar_checklist(
    checklist_data: ChecklistRecebimentoCreate,
    db: Session = Depends(get_db),
):
    recebimento = db.query(Recebimento).filter(Recebimento.id == checklist_data.recebimento_id).first()
    if not recebimento:
        raise HTTPException(status_code=404, detail="Recebimento não encontrado")

    checklist = db.query(ChecklistRecebimentoModel).filter(
        ChecklistRecebimentoModel.recebimento_id == checklist_data.recebimento_id
    ).first()

    if not checklist:
        checklist = ChecklistRecebimentoModel(**checklist_data.model_dump())
        db.add(checklist)
    else:
        for field, value in checklist_data.model_dump().items():
            setattr(checklist, field, value)

    try:
        db.commit()
        db.refresh(checklist)
        return checklist
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar checklist: {str(e)}")

@router.get("/checklist/{recebimento_id}", response_model=ChecklistRecebimentoRead)
def obter_checklist(recebimento_id: int, db: Session = Depends(get_db)):
    checklist = db.query(ChecklistRecebimentoModel).filter(
        ChecklistRecebimentoModel.recebimento_id == recebimento_id
    ).first()
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist não encontrado")
    return checklist
