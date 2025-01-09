from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.recebimento import Recebimento
from app.models.itens_recebimento import ItensRecebimento
from app.models.checklist_recebimento import Checklist_Recebimento
from app.repositories.recebimento_repository import RecebimentoRepository
from app.repositories.itens_recebimento_repository import ItensRecebimentoRepository
from app.schemas.recebimento import RecebimentoSchema, RecebimentoPublic

class RecebimentoService:
    
    def __init__(self):
        self.recebimento_repo = RecebimentoRepository()
        self.itens_recebimento_repo = ItensRecebimentoRepository()

    async def create_recebimento(self, recebimento: RecebimentoSchema, db: AsyncSession, user: User) -> RecebimentoPublic:
        """
        Criação de um novo recebimento.
        """
        db_recebimento = await self.recebimento_repo.create_recebimento(recebimento, db, user)
        
        # Criando checklist e itens relacionados
        await self.create_checklist_e_itens(db_recebimento, db)
        return db_recebimento

    async def list_recebimentos(self, db: AsyncSession, user: User, cliente_id: int | None, offset: int, limit: int):
        """
        Listar todos os recebimentos, com base na paginação.
        """
        return await self.recebimento_repo.get_recebimentos(db, cliente_id, offset, limit)

    async def create_checklist_e_itens(self, recebimento: Recebimento, db: AsyncSession):
        """
        Criar o checklist e os itens relacionados ao recebimento.
        """
        checklist = Checklist_Recebimento(
            ordem_id=recebimento.id,
            datarec_ordem_servicos=recebimento.data_rec_ordem,
            hora_inicial_ordem=recebimento.hora_inicial_ordem,
            referencia_produto=recebimento.referencia_produto,
            nota_interna=f"Nota {recebimento.numero_nota_fiscal}",
            observacao_checklist="Observação inicial",
            status_tarefa="PENDENTE",
            cliente_id=recebimento.cliente_id,
            usuario_id=recebimento.usuario_id,
        )
        db.add(checklist)

        # Adicionar os itens
        for item in recebimento.itens:
            item_db = ItensRecebimento(
                qtd_produto=item.qtd_produto,
                preco_unitario=item.preco_unitario,
                preco_total=item.preco_total,
                referencia_produto=item.referencia_produto,
                status_ordem=item.status_ordem.value,
                produto_id=item.produto_id,
                recebimento_id=recebimento.id,
                funcionario_id=item.funcionario_id,
            )
            db.add(item_db)

        await db.commit()
