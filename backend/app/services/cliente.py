# app/cliente/services.py
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.cliente import Cliente
from app.schemas.cliente import ClienteSchema  # Importando o schema do Cliente

class ClienteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Criar um novo cliente
    async def create(self, cliente_data: ClienteSchema, usuario_logado_id: int) -> Cliente:
        """Cria um novo cliente no banco de dados associado ao usuário logado."""
        if not cliente_data.nome_cliente or not cliente_data.tipo_cliente or not cliente_data.doc_cliente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Os campos tipo_cliente, nome_cliente e doc_cliente são obrigatórios!")

        # Criação do cliente
        novo_cliente = Cliente(**cliente_data.dict())  # Cria uma instância de Cliente com os dados do Pydantic
        novo_cliente.usuario_id = usuario_logado_id  # Associando o cliente ao usuário logado

        try:
            self.db.add(novo_cliente)
            await self.db.commit()  # Persistindo no banco de dados
            await self.db.refresh(novo_cliente)  # Atualizando a instância do cliente com os dados do banco
            return novo_cliente
        except Exception as e:
            await self.db.rollback()  # Faz rollback caso ocorra algum erro
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao criar o cliente: {str(e)}")

    # Listar todos os clientes de um usuário
    async def get_all(self, usuario_logado_id: int) -> List[Cliente]:
        """Retorna todos os clientes associados ao usuário logado."""
        result = await self.db.execute(select(Cliente).filter(Cliente.usuario_id == usuario_logado_id))
        clientes = result.scalars().all()
        if not clientes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum cliente encontrado para o usuário.")
        return clientes

    # Obter um cliente específico pelo ID
    async def get_by_id(self, cliente_id: int, usuario_logado_id: int) -> Cliente:
        """Retorna um cliente pelo ID, apenas se for do usuário logado."""
        result = await self.db.execute(select(Cliente).filter(Cliente.id == cliente_id, Cliente.usuario_id == usuario_logado_id))
        cliente = result.scalars().first()
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado ou não autorizado a acessá-lo.")
        return cliente

    # Atualizar um cliente existente
    async def update(self, cliente_id: int, cliente_data: ClienteSchema, usuario_logado_id: int) -> Cliente:
        """Atualiza os dados de um cliente, somente se for do usuário logado."""
        cliente = await self.get_by_id(cliente_id, usuario_logado_id)
        if cliente:
            cliente.nome_cliente = cliente_data.nome_cliente
            cliente.tipo_cliente = cliente_data.tipo_cliente
            cliente.doc_cliente = cliente_data.doc_cliente
            await self.db.commit()  # Persistindo as mudanças
            await self.db.refresh(cliente)  # Atualizando a instância do cliente com os dados do banco
            return cliente
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado ou não autorizado a atualizá-lo")

    # Excluir um cliente
    async def delete(self, cliente_id: int, usuario_logado_id: int) -> bool:
        """Deleta um cliente pelo ID, somente se for do usuário logado."""
        cliente = await self.get_by_id(cliente_id, usuario_logado_id)
        if cliente:
            await self.db.delete(cliente)
            await self.db.commit()
            return True
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado ou não autorizado a excluí-lo")
