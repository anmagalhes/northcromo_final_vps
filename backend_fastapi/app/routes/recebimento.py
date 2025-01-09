# app/routes/recebimento.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from app.models.user import User
from app.models.cliente import Cliente
from app.models.recebimento.recebimento import Recebimento
from app.models.recebimento.itens_recebimento import ItensRecebimento
from app.models.checklist_recebimento.checklist_recebimento import Checklist_Recebimento

from app.schema.recebimento.recebimento import (
    RecebimentoPublic,
    RecebimentoSchema,
    RecebimentoList,
    RecebimentoUpdate,
    RecebimentoResponse,
)
from app.schema.recebimento.itens_recebimento import ItensRecebimentoSchema
from app.schema.checklist import ChecklistRecebimentoPublic

from core.desp import get_current_user, get_session
from datetime import datetime

router = APIRouter(prefix="/recebimentos", tags=["Recebimentos"])

# Criando uma variável para a dependência com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]

# Função auxiliar para tratar commits e rollbacks (removendo o commit individual)
async def commit_or_rollback(db: AsyncSession, error: bool = False):
    try:
        # A transação já é gerenciada pelo async with
        if error:
            await db.rollback()  # Rollback em caso de erro
        else:
            await db.commit()  # Commit em caso de sucesso
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar dados: {str(e)}")


async def criar_checklist_e_itens(recebimento: Recebimento, db: AsyncSession):
    try:
        hora_inicial = datetime.now()
        # Ajuste dos valores de `cod_produto` e `quantidade` para valores padrões
        cod_produto = recebimento.itens[0].produto_id if recebimento.itens else 1
        quantidade = recebimento.itens[0].qtd_produto if recebimento.itens else 1
        referencia_produto = recebimento.itens[0].referencia_produto if recebimento.itens else "Não Informada"

        # Criação do checklist
        checklist = Checklist_Recebimento(
            ordem_id=recebimento.id,
            datarec_ordem_servicos=recebimento.data_rec_ordem,
            hora_inicial_ordem=hora_inicial,
            referencia_produto=referencia_produto,
            nota_interna=f"Nota {recebimento.numero_nota_fiscal}" if recebimento.numero_nota_fiscal else "Nota Não Informada",
            observacao_checklist="Observação inicial",
            status_tarefa="PENDENTE",
            data_checklist_ordem_servicos=recebimento.data_rec_ordem,
            cliente_id=recebimento.cliente_id,
            usuario_id=recebimento.usuario_id,
            cod_produto=cod_produto,
            quantidade=quantidade
        )
        db.add(checklist)

        # Criação dos itens do recebimento
        for item in recebimento.itens:
            item_db = ItensRecebimento(
                qtd_produto=item.qtd_produto or 1,
                preco_unitario=item.preco_unitario,
                preco_total=item.preco_total,
                referencia_produto=item.referencia_produto or "Não Informada",
                status_ordem=item.status_ordem.value,
                produto_id=item.produto_id,
                recebimento_id=recebimento.id,
                funcionario_id=item.funcionario_id,
            )
            db.add(item_db)

        await commit_or_rollback(db)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar dados: {str(e)}")


@router.post("/", response_model=List[RecebimentoPublic])
async def create_recebimentos(
    recebimentos: List[RecebimentoSchema],
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    created_recebimentos = []  # Lista para armazenar os recebimentos criados

    try:
        # Usando o método síncrono db.begin() para garantir transação
        async with db.begin():
            for recebimento in recebimentos:
                # Criando o objeto Recebimento
                db_recebimento = Recebimento(
                    tipo_ordem=recebimento.tipo_ordem,
                    numero_ordem=recebimento.numero_ordem,
                    recebimento_ordem=recebimento.recebimento_ordem,
                    data_rec_ordem=recebimento.data_rec_ordem,
                    queixa_cliente=recebimento.queixa_cliente,
                    data_prazo_desmont=recebimento.data_prazo_desmont,
                    sv_desmontagem_ordem=recebimento.sv_desmontagem_ordem,
                    sv_montagem_teste_ordem=recebimento.sv_montagem_teste_ordem,
                    limpeza_quimica_ordem=recebimento.limpeza_quimica_ordem,
                    laudo_tecnico_ordem=recebimento.laudo_tecnico_ordem,
                    desmontagem_ordem=recebimento.desmontagem_ordem,
                    cliente_id=recebimento.cliente_id,
                )

                # Adicionando o recebimento à sessão
                db.add(db_recebimento)
                await db.flush()  # Garante que o ID seja atribuído ao objeto

                # Validando e criando os itens do recebimento
                for item in recebimento.itens:
                    if item.qtd_produto is None or item.qtd_produto <= 0:
                        item.qtd_produto = 1  # Ajusta para 1 caso esteja nulo ou zero

                    if item.preco_unitario is None or item.preco_unitario < 0:
                        item.preco_unitario = 0.0  # Ajusta para 0.0 caso esteja nulo ou negativo

                    if item.preco_total is None or item.preco_total < 0:
                        item.preco_total = 0.0  # Ajusta para 0.0 caso esteja nulo ou negativo

                    if not item.referencia_produto:
                        item.referencia_produto = "Não INFORMADO"  # Define como "Não INFORMADO" se estiver vazio

                    if not item.status_ordem:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Status da ordem não pode ser vazio."
                        )
                    if not item.produto_id:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Produto ID é obrigatório."
                        )
                    if not item.funcionario_id:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Funcionário ID é obrigatório."
                        )

                    # Criando o item de recebimento e associando ao recebimento
                    item_db = ItensRecebimento(
                        qtd_produto=item.qtd_produto,
                        preco_unitario=item.preco_unitario,
                        preco_total=item.preco_total,
                        referencia_produto=item.referencia_produto,
                        status_ordem=item.status_ordem,
                        produto_id=item.produto_id,
                        recebimento_id=db_recebimento.id,  # Associando o item ao recebimento
                        funcionario_id=item.funcionario_id,
                    )
                    db.add(item_db)

            await db.commit()  # Commit após a criação de todos os itens e recebimentos

        # Retornando os recebimentos criados
        for db_recebimento in recebimentos:
            created_recebimentos.append(RecebimentoPublic(
                id=db_recebimento.id,
                tipo_ordem=db_recebimento.tipo_ordem,
                numero_ordem=db_recebimento.numero_ordem,
                cliente_id=db_recebimento.cliente_id,
                produtos=db_recebimento.produtos,
                vendedor=db_recebimento.vendedor,
                status_ordem=db_recebimento.status_ordem,
                ordem_checklist=db_recebimento.ordem_checklist,
            ))

        return created_recebimentos

    except SQLAlchemyError as e:
        db.rollback()  # Revertendo transação em caso de erro
        raise HTTPException(status_code=500, detail=f"Erro ao salvar os recebimentos: {str(e)}")


@router.delete("/{recebimento_id}", response_model=RecebimentoResponse)
async def delete_recebimento(
    recebimento_id: int,
    db: DbSession,
    user: Current_user,
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado")

    query = select(Recebimento).where(Recebimento.id == recebimento_id)
    result = await db.execute(query)
    db_recebimento = result.scalars().first()

    if not db_recebimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recebimento não encontrado.")

    query_itens = select(ItensRecebimento).where(ItensRecebimento.recebimento_id == recebimento_id)
    result_itens = await db.execute(query_itens)
    itens = result_itens.scalars().all()

    for item in itens:
        await db.delete(item)

    query_checklist = select(Checklist_Recebimento).where(Checklist_Recebimento.recebimento_id == recebimento_id)
    result_checklist = await db.execute(query_checklist)
    checklist = result_checklist.scalars().first()

    if checklist:
        await db.delete(checklist)

    await db.delete(db_recebimento)

    await commit_or_rollback(db)

    return db_recebimento
