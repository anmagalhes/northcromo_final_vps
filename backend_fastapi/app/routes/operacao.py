from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.operacao import Operacao
from app.models.user import User
from app.schema.operacao import (
    OperacaoPublic,
    OperacaoSchema,
    OperacaoList,
    OperacaoUpdate,
)
from core.desp import get_current_user, get_session

router = APIRouter(prefix="/operacao", tags=["operacao"])

# Criando uma variável para a dependência com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# CRIAR
@router.post("/", response_model=OperacaoPublic)
async def create_operacao(
    operacao: OperacaoSchema,  # Dados de entrada para criar a Operacao
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Criando uma nova Operacao no banco de dados
    db_operacao = Operacao(
        name=operacao.name,
        grupo_operacao=operacao.grupo_operacao,
        usuario_id=user.id,  # Associando a Operacao ao usuário autenticado
    )

    db.add(db_operacao)  # Adicionando a Operacao à sessão do banco
    await db.commit()  # Persistindo a transação
    await db.refresh(
        db_operacao
    )  # Atualizando o objeto com os dados persistidos (como o ID)

    return db_operacao  # Retornando a Operacao criada


# LISTAR Operacoes
@router.get("/", response_model=OperacaoList)
async def list_operacoes(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário atual autenticado
    name: str | None = None,  # Filtro opcional pelo nome
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

    # Criando a consulta para pegar todas as Operacoes
    query = select(Operacao)

    # Filtros de busca
    if name:
        query = query.filter(Operacao.name.ilike(f"%{name}%"))

    # Paginação
    query = query.offset(offset).limit(limit)

    # Executando a consulta
    result = await db.execute(query)
    operacoes = result.unique().scalars().all()

    if not operacoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma Operação encontrada"
        )

    # Retorno dos resultados paginados com o campo 'operacoes'
    return {"Operacaos": operacoes, "offset": offset, "limit": limit}


# ALTERAR
@router.patch("/{operacao_id}", response_model=OperacaoPublic)
async def update_operacao(
    operacao_id: int,  # ID da Operação a ser atualizada
    operacao: OperacaoSchema,  # Dados de entrada para atualizar a Operação
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    operacao_update: OperacaoUpdate,
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se a Operação existe no banco de dados
    query = select(Operacao).where(Operacao.id == operacao_id)
    result = await db.execute(query)
    db_operacao = result.scalars().first()

    if not db_operacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operação não encontrada.",
        )

    # Atualiza os campos com os dados enviados na requisição, se presentes
    update_data = operacao_update.dict(
        exclude_unset=True
    )  # Pega os dados que não são None
    for key, value in update_data.items():
        setattr(db_operacao, key, value)

    # Commit das mudanças no banco de dados
    await db.commit()

    # Refresca o objeto para garantir que ele tenha os dados mais recentes
    await db.refresh(db_operacao)

    # Retorna a Operação atualizada
    return db_operacao
