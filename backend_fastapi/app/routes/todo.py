# app/controllers/task_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy.orm import Session

from core.desp import get_session, get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

@router.post('/', response_model=Todo)
def create_todo(todo: TodoSchema):
    return 