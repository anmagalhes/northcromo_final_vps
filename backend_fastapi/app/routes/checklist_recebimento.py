# app/controllers/checklist_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy.orm import Session

from core.desp import get_session, get_current_user

from pydantic import BaseModel

router = APIRouter()


class ChecklistCreate(BaseModel):
    nome: str
    descricao: str
    tarefa_id: int


@router.post("/checklists/")
def create_checklist(checklist: ChecklistCreate,  db: AsyncSession = Depends(get_session)):
    db_checklist = checklist(**checklist.dict())
    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)
    return db_checklist
