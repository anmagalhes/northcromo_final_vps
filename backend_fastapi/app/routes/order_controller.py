# app/controllers/order_controller.py
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.services import order_service
from app.schema.order_schem import OrderSchema
from app.core.desp import get_session, get_current_user

# BYpass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

# Corrigindo o nome do método `inherit_cache` (ao invés de `inrerit_cache`)
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
# Fim BYpass

router = APIRouter()

# Função de dependência para obter a sessão do banco de dados


@router.post("/orders/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderSchema, db: AsyncSession = Depends(get_session)):
    """
    Cria um novo pedido (order) na base de dados.

    - **order**: Dados do pedido a ser criado.
    - **db**: Sessão do banco de dados, injetada automaticamente via dependência.

    Retorna o pedido recém-criado com o código de status `201 Created`.
    Caso haja algum erro durante a criação, um erro 400 (Bad Request) será retornado.
    """
    try:
        # Chamando o serviço para criar o pedido
        return await order_service.create_order(db=db, order=order)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/orders/", response_model=List[OrderSchema])
async def get_orders(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    """
    Recupera a lista de pedidos com base na paginação definida pelos parâmetros `skip` e `limit`.

    - **skip**: Número de pedidos a ser pulado (default: 0).
    - **limit**: Número máximo de pedidos a ser retornado (default: 10).
    - **db**: Sessão do banco de dados, injetada automaticamente via dependência.

    Retorna uma lista de pedidos (orders) com base nos critérios de paginação.
    Caso haja algum erro durante a recuperação dos pedidos, um erro 400 (Bad Request) será retornado.
    """
    try:
        # Chamando o serviço para listar os pedidos com paginação
        return await order_service.get_orders(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/orders/{order_id}", response_model=OrderSchema)
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_session)):
    """
    Recupera um pedido específico com base no `order_id`.

    - **order_id**: ID do pedido a ser recuperado.
    - **db**: Sessão do banco de dados, injetada automaticamente via dependência.

    Retorna os detalhes do pedido se encontrado. Caso contrário, retorna um erro `404 Not Found`.
    """
    try:
        # Chamando o serviço para obter um pedido pelo ID
        order = await order_service.get_order_by_id(db=db, order_id=order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/orders/{order_id}", response_model=OrderSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_order(order_id: int, order: OrderSchema, db: AsyncSession = Depends(get_session)):
    """
    Atualiza os dados de um pedido específico com base no `order_id`.

    - **order_id**: ID do pedido a ser atualizado.
    - **order**: Dados do pedido a ser atualizado.
    - **db**: Sessão do banco de dados, injetada automaticamente via dependência.

    Retorna o pedido atualizado. Caso o pedido não seja encontrado, retorna um erro `404 Not Found`.
    """
    try:
        # Chamando o serviço para atualizar o pedido
        updated_order = await order_service.update_order(db=db, order_id=order_id, order=order)
        if not updated_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return updated_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_session)):
    """
    Exclui um pedido específico com base no `order_id`.

    - **order_id**: ID do pedido a ser excluído.
    - **db**: Sessão do banco de dados, injetada automaticamente via dependência.

    Retorna `204 No Content` se a exclusão for bem-sucedida. Caso o pedido não seja encontrado, retorna um erro `404 Not Found`.
    """
    try:
        # Chamando o serviço para deletar o pedido
        deleted = await order_service.delete_order(db=db, order_id=order_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)  # Sem conteúdo na resposta
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
