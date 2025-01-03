# app/controllers/componente_controller.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.postotrabalho import Postotrabalho
from app.models.user import User
from app.schema.postotrabalho import PostotrabalhoPublic, PostotrabalhoSchema,  PostotrabalhoList, PostotrabalhoUpdate
from core.desp import get_current_user, get_session

router = APIRouter(prefix="/postotrabalho", tags=["postotrabalho"])

# Criando uma variável para a dependência com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# CRIAR
@router.post("/", response_model=PostotrabalhoPublic)
async def create_postotrabalho(
    postotrabalho: PostotrabalhoSchema,  # Dados de entrada para criar o Componente
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Criando um novo Componente no banco de dados
    db_postotrabalho = Postotrabalho(
        name=postotrabalho.name,
        usuario_id=user.id,  # Associando o Componente ao usuário autenticado
    )

    db.add(db_postotrabalho)  # Adicionando o Componente à sessão do banco
    await db.commit()  # Persistindo a transação
    await db.refresh(db_postotrabalho)  # Atualizando o objeto com os dados persistidos (como o ID)

    return db_postotrabalho  # Retornando o Componente criado

# LISTAR Componentes
@router.get("/", response_model=PostotrabalhoList)
async def list_componentes(
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

    # Criando a consulta para pegar todos os Componentes
    query = select(Postotrabalho)

    # Filtros de busca
    if name:
        query = query.filter(Postotrabalho.name.ilike(f"%{name}%"))

    # Paginação
    query = query.offset(offset).limit(limit)

    # Executando a consulta
    result = await db.execute(query)
    postotrabalhos = result.unique().scalars().all()
    
    if not postotrabalhos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum Componente encontrado"
        )

    # Retorno dos resultados paginados com o campo 'componentes'
    return {"postotrabalhos": postotrabalhos, "offset": offset, "limit": limit}

# ALTERAR
@router.patch("/{postotrabalho_id}", response_model=PostotrabalhoPublic)
async def update_componente(
    componente_id: int,  # ID do Componente a ser atualizado
    componente: PostotrabalhoSchema,  # Dados de entrada para atualizar o Componente
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    componente_update: PostotrabalhoUpdate,
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o Componente existe no banco de dados
    query = select(Postotrabalho).where(Postotrabalho.id == componente_id)
    result = await db.execute(query)
    db_postotrabalho = result.scalars().first()

    if not db_postotrabalho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Componente não encontrado.",
        )

    # Atualiza os campos com os dados enviados na requisição, se presentes
    update_data = componente_update.dict(exclude_unset=True)  # Pega os dados que não são None
    for key, value in update_data.items():
        setattr(db_postotrabalho, key, value)

    # Commit das mudanças no banco de dados
    await db.commit()

    # Refresca o objeto para garantir que ele tenha os dados mais recentes
    await db.refresh(db_postotrabalho)

    # Retorna o Componente atualizado
    return db_postotrabalho
