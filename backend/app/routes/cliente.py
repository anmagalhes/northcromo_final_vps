# app/routes/cliente.py
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.cliente_model import Cliente
from app.models.user import User
from app.core.desp import get_session, get_current_user

# BYpass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

# Corrigindo o nome do método `inherit_cache` (ao invés de `inrerit_cache`)
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
# Fim BYpass

api_router = APIRouter()


# Rota para criar um novo cliente
@api_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ClienteSchema)
async def criar_cliente(cliente_data: ClienteSchema, usuario_logado: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    """
    Cria um novo cliente. A operação está associada ao usuário logado.
    """
    try:
        service = ClienteService(db)
        # Criação do cliente via serviço
        novo_cliente = await service.create(cliente_data, usuario_logado.id)
        return novo_cliente
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar cliente"
        )

# Rota para listar todos os clientes do usuário logado
@api_router.get("/", response_model=List[ClienteSchema])
async def get_all_clientes(usuario_logado: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    """Retorna todos os clientes cadastrados para o usuário logado."""
    service = ClienteService(db)
    return await service.get_all(usuario_logado)

# Rota para pegar detalhes de um cliente específico
@api_router.get("/{id}", response_model=ClienteSchema, status_code=status.HTTP_200_OK)
async def get_cliente_details(id: int, usuario_logado: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    """Retorna os detalhes de um cliente pelo ID, somente se for do usuário logado."""
    service = ClienteService(db)
    cliente = await service.get_by_id(id, usuario_logado)
    if not cliente:
        raise HTTPException(
            detail="Cliente não encontrado ou não autorizado a acessá-lo",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return cliente

# Rota para atualizar um cliente
@api_router.put("/{id}", response_model=ClienteSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_cliente_details(id: int, cliente_data: ClienteSchema, usuario_logado: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    """Atualiza os dados de um cliente específico, somente se for do usuário logado."""
    service = ClienteService(db)
    updated_cliente = await service.update(id, cliente_data, usuario_logado)
    if not updated_cliente:
        raise HTTPException(
            detail="Cliente não encontrado ou não autorizado a atualizá-lo",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return updated_cliente

# Rota para deletar um cliente
@api_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente_by_id(id: int, usuario_logado: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    """Deleta um cliente pelo ID, somente se for do usuário logado."""
    service = ClienteService(db)
    deleted = await service.delete(id, usuario_logado)
    if not deleted:
        raise HTTPException(
            detail="Cliente não encontrado ou não autorizado a excluí-lo",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Sem conteúdo na resposta
