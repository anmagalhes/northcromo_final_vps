# app/controllers/task_controller.py
from typing import Annotated

from core.desp import get_current_user, get_session
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import User
from app.models.todo import Todo, TodoState
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.schema.todo import TodoPublic, TodoSchema, TodoList, TodoUpdate

router = APIRouter(prefix="/todo", tags=["todos"])

# Criando uma variável para a dependência com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# CRIAR 
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
        usuario_id=user.id,  # Associando o Todo ao usuário autenticado
    )

    db.add(db_todo)  # Adicionando o Todo à sessão do banco
    await db.commit()  # Persistindo a transação
    await db.refresh(
        db_todo
    )  # Atualizando o objeto com os dados persistidos (como o ID)

    return db_todo  # Retornando o Todo criado

# LISTA
@router.get("/", response_model=TodoList)
async def list_todos(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário atual autenticado
    titulo: str | None = None,
    descricao: str | None = None,
    status: str | None = None,
    offset: int = 0,  # Valor padrão para a paginação
    limit: int = 10,  # Valor padrão para a paginação
):
    if offset < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset não pode ser negativo.",
        )
    if limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limite deve ser maior que zero.",
        )
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limite não pode ser maior que 100.",
        )

    # Criando a consulta para pegar todos os Todos, não mais filtrando pelo usuário
    query = select(Todo)  # Apenas os todos do usuário autenticado

    # Filtros de busca
    if titulo:
        query = query.filter(Todo.titulo.ilike(f"%{titulo}%"))

    if descricao:
        query = query.filter(Todo.descricao.ilike(f"%{descricao}%"))

    if status:
        query = query.filter(Todo.status == status)

    # Paginação
    query = query.offset(offset).limit(limit)

    # Executando a consulta
    result = await db.execute(query)
    todos = (
        result.unique().scalars().all()
    )  # Pega todos os resultados como objetos Todo

    if not todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum Todo encontrado"
        )

    # Retorno dos resultados paginados
    return {"todos": todos, "offset": offset, "limit": limit}


# ALTERAR
@router.patch("/{todo_id}", response_model=TodoPublic)
async def update_todo(
    todo_id: int,  # ID do Todo a ser atualizado
    todo: TodoSchema,  # Dados de entrada para atualizar o Todo
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    todo_update: TodoUpdate,
):

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o Todo existe no banco de dados
    query = select(Todo).where(Todo.id == todo_id)
    result = await db.execute(query)
    db_todo = result.scalars().first()

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo não encontrado ou você não tem permissão para alterá-lo.",
        )
    
    # Atualiza os campos com os dados enviados na requisição, se presentes
    update_data = todo_update.dict(exclude_unset=True)  # Pega os dados que não são None
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    # Commit das mudanças no banco de dados (não precisa adicionar o objeto novamente à sessão)
    await db.commit()

    # Refresca o objeto para garantir que ele tenha os dados mais recentes
    await db.refresh(db_todo)

    # Retorna o Todo atualizado
    return db_todo