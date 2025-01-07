#app/routes/funcionario.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.funcionario import Funcionario
from app.models.user import User
from app.schema.funcionario import (
    FuncionarioPublic,
    FuncionarioSchema,
    FuncionarioList,
    FuncionarioUpdate,
)
from core.desp import get_current_user, get_session

router = APIRouter(prefix="/funcionario", tags=["funcionarios"])

# Criando variáveis para dependências com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# CRIAR Funcionario
@router.post("/", response_model=FuncionarioPublic)
async def create_funcionario(
    funcionario: FuncionarioSchema,  # Dados de entrada para criar o Funcionario
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Criando um novo Funcionario no banco de dados
    db_funcionario = Funcionario(
        nome=funcionario.nome,
        cargo=funcionario.cargo,
        usuario_id=user.id,  # Associando o Funcionario ao usuário autenticado
    )

    db.add(db_funcionario)  # Adicionando o Funcionario à sessão do banco
    await db.commit()  # Persistindo a transação
    await db.refresh(db_funcionario)  # Atualizando o objeto com os dados persistidos (como o ID)

    return db_funcionario  # Retornando o Funcionario criado


# LISTAR Funcionarios
@router.get("/", response_model=FuncionarioList)
async def list_funcionarios(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário atual autenticado
    nome: str | None = None,  # Filtro opcional pelo nome
    offset: int = 0,  # Valor padrão para a paginação
    limit: int = 10,  # Valor padrão para a paginação
):
    # Verificações de validação de offset e limit
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

    # Criando a consulta para pegar todos os Funcionarios
    query = select(Funcionario)

    # Filtros de busca
    if nome:
        query = query.filter(Funcionario.nome.ilike(f"%{nome}%"))

    # Paginação
    query = query.offset(offset).limit(limit)

    # Executando a consulta
    result = await db.execute(query)
    funcionarios = result.unique().scalars().all()

    if not funcionarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum Funcionario encontrado"
        )

    # Retorno dos resultados paginados com o campo 'funcionarios'
    return {"funcionarios": funcionarios, "offset": offset, "limit": limit}


# ALTERAR Funcionario
@router.patch("/{funcionario_id}", response_model=FuncionarioPublic)
async def update_funcionario(
    funcionario_id: int,  # ID do Funcionario a ser atualizado
    funcionario: FuncionarioSchema,  # Dados de entrada para atualizar o Funcionario
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    funcionario_update: FuncionarioUpdate,
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o Funcionario existe no banco de dados
    query = select(Funcionario).where(Funcionario.id == funcionario_id)
    result = await db.execute(query)
    db_funcionario = result.scalars().first()

    if not db_funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionario não encontrado.",
        )

    # Atualiza os campos com os dados enviados na requisição, se presentes
    update_data = funcionario_update.dict(
        exclude_unset=True
    )  # Pega os dados que não são None
    for key, value in update_data.items():
        setattr(db_funcionario, key, value)

    # Commit das mudanças no banco de dados
    await db.commit()

    # Refresca o objeto para garantir que ele tenha os dados mais recentes
    await db.refresh(db_funcionario)

    # Retorna o Funcionario atualizado
    return db_funcionario


# DELETAR Funcionario
@router.delete("/{funcionario_id}", response_model=FuncionarioPublic)
async def delete_funcionario(
    funcionario_id: int,  # ID do Funcionario a ser deletado
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o Funcionario existe no banco de dados
    query = select(Funcionario).where(Funcionario.id == funcionario_id)
    result = await db.execute(query)
    db_funcionario = result.scalars().first()

    if not db_funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionario não encontrado.",
        )

    # Deleta o Funcionario do banco de dados
    await db.delete(db_funcionario)
    await db.commit()

    return db_funcionario  # Retorna o Funcionario deletado
