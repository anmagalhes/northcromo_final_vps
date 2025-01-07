# app/routes/cliente.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.cliente import Cliente
from app.models.user import User
from app.schema.cliente import (
    ClientePublic,
    ClienteSchema,
    ClienteList,
    ClienteUpdate,
)
from core.desp import get_current_user, get_session

router = APIRouter(prefix="/cliente", tags=["clientes"])

# Criando variáveis para dependências com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# CRIAR Cliente
@router.post("/", response_model=ClientePublic)
async def create_cliente(
    cliente: ClienteSchema,  # Dados de entrada para criar o Cliente
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Criando um novo Cliente no banco de dados
    db_cliente = Cliente(
        nome_cliente=cliente.nome_cliente,
        doc_cliente=cliente.doc_cliente,
        endereco_cliente=cliente.endereco_cliente,
        num_cliente=cliente.num_cliente,
        bairro_cliente=cliente.bairro_cliente,
        cidade_cliente=cliente.cidade_cliente,
        uf_cliente=cliente.uf_cliente,
        cep_cliente=cliente.cep_cliente,
        telefone_cliente=cliente.telefone_cliente,
        usuario_id=user.id,  # Associando o Cliente ao usuário autenticado
    )

    db.add(db_cliente)  # Adicionando o Cliente à sessão do banco
    await db.commit()  # Persistindo a transação
    await db.refresh(
        db_cliente
    )  # Atualizando o objeto com os dados persistidos (como o ID)

    return db_cliente  # Retornando o Cliente criado


# LISTAR Clientes
@router.get("/", response_model=ClienteList)
async def list_clientes(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário atual autenticado
    nome_cliente: str | None = None,  # Filtro opcional pelo nome
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

    # Criando a consulta para pegar todos os Clientes
    query = select(Cliente)

    # Filtros de busca
    if nome_cliente:
        query = query.filter(Cliente.nome_cliente.ilike(f"%{nome_cliente}%"))

    # Paginação
    query = query.offset(offset).limit(limit)

    # Executando a consulta
    result = await db.execute(query)
    clientes = result.unique().scalars().all()

    if not clientes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum Cliente encontrado"
        )

    # Retorno dos resultados paginados com o campo 'clientes'
    return {"clientes": clientes, "offset": offset, "limit": limit}


# ALTERAR Cliente
@router.patch("/{cliente_id}", response_model=ClientePublic)
async def update_cliente(
    cliente_id: int,  # ID do Cliente a ser atualizado
    cliente: ClienteSchema,  # Dados de entrada para atualizar o Cliente
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    cliente_update: ClienteUpdate,
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o Cliente existe no banco de dados
    query = select(Cliente).where(Cliente.id == cliente_id)
    result = await db.execute(query)
    db_cliente = result.scalars().first()

    if not db_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )

    # Atualiza os campos com os dados enviados na requisição, se presentes
    update_data = cliente_update.dict(
        exclude_unset=True
    )  # Pega os dados que não são None
    for key, value in update_data.items():
        setattr(db_cliente, key, value)

    # Commit das mudanças no banco de dados
    await db.commit()

    # Refresca o objeto para garantir que ele tenha os dados mais recentes
    await db.refresh(db_cliente)

    # Retorna o Cliente atualizado
    return db_cliente


# DELETAR Cliente (opcional)
@router.delete("/{cliente_id}", response_model=ClientePublic)
async def delete_cliente(
    cliente_id: int,  # ID do Cliente a ser deletado
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o Cliente existe no banco de dados
    query = select(Cliente).where(Cliente.id == cliente_id)
    result = await db.execute(query)
    db_cliente = result.scalars().first()

    if not db_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )

    # Deleta o Cliente do banco de dados
    await db.delete(db_cliente)
    await db.commit()

    return db_cliente  # Retorna o Cliente deletado
