# app/controllers/checklist_controller.py
from core.desp import get_session
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class ChecklistCreate(BaseModel):
    nome: str
    descricao: str
    tarefa_id: int


@router.post("/checklists/")
def create_checklist(
    checklist: ChecklistCreate, db: AsyncSession = Depends(get_session)
):
    db_checklist = checklist(**checklist.dict())
    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)
    return db_checklist
