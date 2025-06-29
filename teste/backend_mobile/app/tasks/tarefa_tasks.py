from celery import shared_task
from app.database.session import async_session
from app.api.models.tarefa import Tarefa
from app.api.models.enums import StatusTarefaEnum
from app.utils.datetime import utcnow

@shared_task
def criar_tarefa_depois(recebimento_id: int, referencia_produto: str = ""):
    import asyncio

    async def _criar():
        async with async_session() as session:
            tarefa = Tarefa(
                recebimento_id=recebimento_id,
                data_rec_ordem=utcnow(),
                qtde_servico=1,
                id_servico=1,
                id_servico2=None,
                id_operacao=1,
                desc_servico_produto="Serviço criado automaticamente",
                obs="Checklist finalizado",
                status=StatusTarefaEnum.PENDENTE,
                referencia_produto=referencia_produto,
                nota_interna="",
                data_checklist_ordem=utcnow()
            )
            session.add(tarefa)
            await session.commit()

    asyncio.run(_criar())
