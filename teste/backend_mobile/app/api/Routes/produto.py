from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.database.session import get_async_session
from app.api.models.produto import Produto
from app.Schema.produto_schema import ProdutoCreate, ProdutoRead
import asyncio
from sqlalchemy.orm import selectinload

from app.api.models.fornecedor import Fornecedor
from enum import Enum as PyEnum
import traceback

from fastapi.encoders import jsonable_encoder

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.post("/produto", response_model=ProdutoRead)
async def criar_produto(produto_data: ProdutoCreate, db: AsyncSession = Depends(get_async_session)):
    grupo_valor = produto_data.grupo_id.value if isinstance(produto_data.grupo_id, PyEnum) else produto_data.grupo_id

    try:
        produto = Produto(
            cod_produto=produto_data.cod_produto,
            produto_nome=produto_data.produto_nome,
            componente_id=produto_data.componente_id,
            operacao_id=produto_data.operacao_id,
            und_servicos=produto_data.und_servicos,
            grupo_id=grupo_valor,
            tipo_produto=produto_data.tipo_produto,
            posto_trabalho_id=produto_data.posto_trabalho_id,
            fornecedores=[],
            data=produto_data.data,
        )

        # Adiciona fornecedores relacionados
        if produto_data.fornecedores:
            for fornecedor_id in produto_data.fornecedores:
                fornecedor = await db.get(Fornecedor, fornecedor_id)
                if fornecedor:
                    produto.fornecedores.append(fornecedor)

        db.add(produto)
        await db.commit()
        await db.refresh(produto)

        await manager.broadcast("Produto criado")

        return produto

    except SQLAlchemyError as e:
        await db.rollback()
        traceback.print_exc()  # imprime stacktrace no console
        raise HTTPException(status_code=500, detail=f"Erro ao salvar produto: {str(e)}")

# Listar produtos com relacionamento carregado
@router.get("/produto", response_model=List[ProdutoRead])
async def listar_produtos(db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(
            select(Produto)
            .options(
                selectinload(Produto.fornecedores),
                selectinload(Produto.componente),
                selectinload(Produto.operacao),
                selectinload(Produto.posto_trabalho)
            )  # carregando relacionamento fornecedores
        )
        produtos = result.scalars().all()

        json_produtos = jsonable_encoder(produtos)
        print(f"Produtos retornados (JSON): {json_produtos}")

        return produtos
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produtos: {str(e)}")

# Buscar produto por ID com relacionamento carregado
@router.get("/produto/{produto_id}", response_model=ProdutoRead)
async def buscar_produto(produto_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(
            select(Produto)
            .options(
                selectinload(Produto.fornecedores),  # carregando relacionamento fornecedores
                selectinload(Produto.componente),
                selectinload(Produto.operacao),
                selectinload(Produto.posto_trabalho)
            )
            .where(Produto.id == produto_id)
        )
        produto = result.scalars().first()
        print(f"Produtos retornados: {produto}")

        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        return produto
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produto: {str(e)}")


# Atualizar produto
@router.put("/produto/{produto_id}", response_model=ProdutoRead)
async def atualizar_produto(
    produto_id: int, produto_data: ProdutoCreate, db: AsyncSession = Depends(get_async_session)
):
    try:
        result = await db.execute(select(Produto).where(Produto.id == produto_id))
        produto = result.scalars().first()

        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        produto.cod_produto = produto_data.cod_produto
        produto.produto_nome = produto_data.produto_nome
        produto.componente_id = produto_data.componente_id
        produto.operacao_id = produto_data.operacao_id
        produto.und_servicos = produto_data.und_servicos
        if isinstance(produto_data.grupo_id, PyEnum):
            produto.grupo_id = produto_data.grupo_id.value
        else:
            produto.grupo_id = produto_data.grupo_id

        produto.tipo_produto = produto_data.tipo_produto
        produto.posto_trabalho_id = produto_data.posto_trabalho_id

        await db.commit()
        await db.refresh(produto)

        await manager.broadcast("Produto atualizado")  # Notifica clientes

        return produto

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar produto: {str(e)}")


# Deletar produto
@router.delete("/produto/{produto_id}", status_code=204)
async def deletar_produto(produto_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Produto).where(Produto.id == produto_id))
        produto = result.scalars().first()

        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        await db.delete(produto)
        await db.commit()

        await manager.broadcast("Produto excluído")  # Notifica clientes

        return

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar produto: {str(e)}")


# WebSocket para notificações de produtos
@router.websocket("/ws/produtos")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # mantém conexão ativa
            # opcionalmente processe 'data' aqui ou ignore
    except WebSocketDisconnect:
        manager.disconnect(websocket)
