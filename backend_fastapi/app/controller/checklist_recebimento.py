# app/controllers/checklist_controller.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import checklist
from pydantic import BaseModel

router = APIRouter()


class ChecklistCreate(BaseModel):
    nome: str
    descricao: str
    tarefa_id: int


@router.post("/checklists/")
def create_checklist(checklist: ChecklistCreate, db: Session = Depends(get_db)):
    db_checklist = checklist(**checklist.dict())
    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)
    return db_checklist
