# app/routes/produto.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.produto import Produto
from app.models.user import User
from app.schema.produto import ProdutoPublic, ProdutoSchema, ProdutoList, ProdutoUpdate
from core.desp import get_current_user, get_session

router = APIRouter(prefix="/produto", tags=["produtos"])

# Criando variáveis para dependências com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# CRIAR Produto
@router.post("/", response_model=ProdutoPublic)
async def create_produto(
    produto: ProdutoSchema,  # Dados de entrada para criar o Produto
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Criando um novo Produto no banco de dados
    db_produto = Produto(
        codigo=produto.codigo,
        nome_produto=produto.nome_produto,
        und_servicos=produto.und_servicos,
        usuario_id=user.id,  # Associando o Produto ao usuário autenticado
    )

    db.add(db_produto)  # Adicionando o Produto à sessão do banco
    await db.commit()  # Persistindo a transação
    await db.refresh(
        db_produto
    )  # Atualizando o objeto com os dados persistidos (como o ID)

    return db_produto  # Retornando o Produto criado


# LISTAR Produtos
@router.get("/", response_model=ProdutoList)
async def list_produtos(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário atual autenticado
    nome_produto: str | None = None,  # Filtro opcional pelo nome
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

    # Criando a consulta para pegar todos os Produtos
    query = select(Produto)

    # Filtros de busca
    if nome_produto:
        query = query.filter(Produto.nome_produto.ilike(f"%{nome_produto}%"))

    # Paginação
    query = query.offset(offset).limit(limit)

    # Executando a consulta
    result = await db.execute(query)
    produtos = result.unique().scalars().all()

    if not produtos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum Produto encontrado"
        )

    # Retorno dos resultados paginados com o campo 'produtos'
    return {"produtos": produtos, "offset": offset, "limit": limit}


# ALTERAR Produto
@router.patch("/{produto_id}", response_model=ProdutoPublic)
async def update_produto(
    produto_id: int,  # ID do Produto a ser atualizado
    produto_update: ProdutoUpdate,  # Dados de entrada para atualizar o Produto
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o Produto existe no banco de dados
    query = select(Produto).where(Produto.id == produto_id)
    result = await db.execute(query)
    db_produto = result.scalars().first()

    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    # Atualiza os campos com os dados enviados na requisição, se presentes
    update_data = produto_update.dict(
        exclude_unset=True
    )  # Pega os dados que não são None
    for key, value in update_data.items():
        setattr(db_produto, key, value)

    # Commit das mudanças no banco de dados
    await db.commit()

    # Refresca o objeto para garantir que ele tenha os dados mais recentes
    await db.refresh(db_produto)

    # Retorna o Produto atualizado
    return db_produto


# DELETAR Produto
@router.delete("/{produto_id}", response_model=ProdutoPublic)
async def delete_produto(
    produto_id: int,  # ID do Produto a ser deletado
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o Produto existe no banco de dados
    query = select(Produto).where(Produto.id == produto_id)
    result = await db.execute(query)
    db_produto = result.scalars().first()

    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    # Deleta o Produto do banco de dados
    await db.delete(db_produto)
    await db.commit()

    return db_produto  # Retorna o Produto deletado
