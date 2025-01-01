# app/controllers/task_controller.py
from typing import Annotated

from core.desp import get_current_user, get_session
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.todo import TodoPublic, TodoSchema

router = APIRouter(prefix="/todo", tags=["todo"])

# Criando uma variável para a dependência com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


@router.post("/", response_model=TodoPublic)
async def create_todo(
    todo: TodoSchema,  # Dados de entrada para criar o Todo
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário atual autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Criando um novo Todo no banco de dados
    db_todo = Todo(
        titulo=todo.titulo,
        descricao=todo.descricao,
        status=todo.status,
        owner_id=user.id,  # Associando o Todo ao usuário autenticado
    )

    db.add(db_todo)  # Adicionando o Todo à sessão do banco
    await db.commit()  # Persistindo a transação
    await db.refresh(
        db_todo
    )  # Atualizando o objeto com os dados persistidos (como o ID)

    return db_todo  # Retornando o Todo criado
