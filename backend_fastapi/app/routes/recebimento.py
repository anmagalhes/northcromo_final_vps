from datetime import datetime
from typing import Annotated, List

import pytz
from core.desp import get_current_user, get_session
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.checklist_recebimento.checklist_recebimento import Checklist_Recebimento
from app.models.cliente import Cliente
from app.models.recebimento.foto_recebimento import FotoRecebimento
from app.models.recebimento.itens_recebimento import ItensRecebimento
from app.models.recebimento.recebimento import Recebimento
from app.models.user import User
from app.schema.recebimento.itens_recebimento import (
    ItensRecebimentoList,
    ItensRecebimentoPublic,
    ItensRecebimentoSchema,
    ItensRecebimentoUpdate,
)
from app.schema.recebimento.recebimento import (
    RecebimentoPublic,
    RecebimentoResponse,
    RecebimentoSchema,
    SimNaoEnum,
    StatusOrdemEnum
)

# Definir o fuso horário de São Paulo
sp_tz = pytz.timezone("America/Sao_Paulo")

router = APIRouter(prefix="/recebimentos", tags=["Recebimentos"])

# Criando uma variável para a dependência com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]  # Renomeado para CurrentUser


# Ajustando a transação assíncrona
async def commit_or_rollback(db: AsyncSession, error: bool = False):
    try:
        if error:
            await db.rollback()  # Rollback em caso de erro
        else:
            await db.commit()  # Commit em caso de sucesso
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar dados: {str(e)}")


async def criar_checklist_e_itens(recebimento: Recebimento, db: AsyncSession):
    try:
        hora_inicial = datetime.now()
        cod_produto = recebimento.itens[0].produto_id if recebimento.itens else 1
        quantidade = recebimento.itens[0].qtd_produto if recebimento.itens else 1
        referencia_produto = (
            recebimento.itens[0].referencia_produto
            if recebimento.itens
            else "Não Informada"
        )

        checklist = Checklist_Recebimento(
            ordem_id=recebimento.id,
            datarec_ordem_servicos=recebimento.data_rec_ordem,
            hora_inicial_ordem=hora_inicial,
            referencia_produto=referencia_produto,
            nota_interna=(
                f"Nota {recebimento.numero_nota_fiscal}"
                if recebimento.numero_nota_fiscal
                else "Nota Não Informada"
            ),
            observacao_checklist="Observação inicial",
            status_tarefa="PENDENTE",
            data_checklist_ordem_servicos=recebimento.data_rec_ordem,
            cliente_id=recebimento.cliente_id,
            usuario_id=recebimento.usuario_id,
            cod_produto=cod_produto,
            quantidade=quantidade,
        )
        db.add(checklist)

        for item in recebimento.itens:
            item_db = ItensRecebimento(
                qtd_produto=item.qtd_produto or 1,
                preco_unitario=item.preco_unitario,
                preco_total=item.preco_total,
                referencia_produto=item.referencia_produto or "Não Informada",
                status_ordem=StatusOrdemEnum(item.status_ordem).value,
                produto_id=item.produto_id,
                recebimento_id=recebimento.id,
                funcionario_id=item.funcionario_id,
            )
            db.add(item_db)

        await commit_or_rollback(db)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar dados: {str(e)}")


async def validar_cliente(cliente_id: int, db: AsyncSession):
    query_cliente = select(Cliente).where(Cliente.id == cliente_id)
    result_cliente = await db.execute(query_cliente)
    cliente = result_cliente.scalars().first()

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado."
        )
    return cliente


@router.post("/", response_model=List[RecebimentoPublic])
async def create_recebimentos(
    recebimentos: List[RecebimentoSchema],
    db: DbSession,
    user: CurrentUser,
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    created_recebimentos = []

    try:
        async with db.begin():  # Iniciar a transação
            for recebimento in recebimentos:
                # Validação do cliente
                cliente = await validar_cliente(recebimento.cliente_id, db)

                # Criação do objeto de recebimento no banco de dados
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
                    usuario_id=user.id,
                    status_ordem=recebimento.status_ordem.value,  # Convertendo para string
                    created_at=datetime.now(sp_tz),  # Converte para string ISO 8601
                    updated_at=datetime.now(sp_tz),  # Converte para string ISO 8601
                )
                db.add(db_recebimento)
                await db.flush()  # Necessário para garantir que o ID seja gerado

                # Adicionar itens ao recebimento
                for item in recebimento.itens:
                    item_db = ItensRecebimento(
                        qtd_produto=item.qtd_produto,
                        preco_unitario=item.preco_unitario,
                        preco_total=item.preco_total,
                        referencia_produto=item.referencia_produto,
                        status_ordem=item.status_ordem.value,
                        produto_id=item.produto_id,
                        recebimento_id=db_recebimento.id,
                        funcionario_id=item.funcionario_id,
                    )
                    db.add(item_db)

                # Aqui você pode incluir os produtos associados ao recebimento
                produtos = [item.produto_id for item in recebimento.itens]

            # Commit da transação se tudo ocorreu bem
            await commit_or_rollback(db)

        # Preparar a resposta com os dados corretos
        for db_recebimento in recebimentos:
            created_recebimentos.append(
                RecebimentoPublic(
                    id=db_recebimento.id,
                    tipo_ordem=db_recebimento.tipo_ordem,
                    numero_ordem=db_recebimento.numero_ordem,
                    cliente_id=db_recebimento.cliente_id,
                    status_ordem=db_recebimento.status_ordem,
                    produtos=produtos,  # Garantir que os produtos sejam listados corretamente
                    data_rec_ordem=db_recebimento.data_rec_ordem.isoformat(),  # Converter para string
                    created_at=datetime.now(sp_tz),  # Ajustado para São Paulo
                    updated_at=datetime.now(sp_tz),  # Ajustado para São Paulo
                    itens=[
                        {
                            "id": item.id,
                            "qtd_produto": item.qtd_produto,
                            "preco_unitario": item.preco_unitario,
                            "preco_total": item.preco_total,
                            "referencia_produto": item.referencia_produto,
                            "status_ordem": item.status_ordem,
                            "produto_id": item.produto_id,
                            "funcionario_id": item.funcionario_id,
                        }
                        for item in db_recebimento.itens
                    ],  # Preenchendo a lista de itens
                )
            )
        return created_recebimentos

    except SQLAlchemyError as e:
        # Em caso de erro, faz o rollback
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar os recebimentos: {str(e)}",
        )


@router.delete("/{recebimento_id}", response_model=RecebimentoResponse)
async def delete_recebimento(
    recebimento_id: int,
    db: DbSession,
    user: CurrentUser,
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    query = select(Recebimento).where(Recebimento.id == recebimento_id)
    result = await db.execute(query)
    db_recebimento = result.scalars().first()

    if not db_recebimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recebimento não encontrado."
        )

    # Deletar itens e checklist
    query_itens = select(ItensRecebimento).where(
        ItensRecebimento.recebimento_id == recebimento_id
    )
    result_itens = await db.execute(query_itens)
    itens = result_itens.scalars().all()

    for item in itens:
        await db.delete(item)

    query_checklist = select(Checklist_Recebimento).where(
        Checklist_Recebimento.recebimento_id == recebimento_id
    )
    result_checklist = await db.execute(query_checklist)
    checklist = result_checklist.scalars().first()

    if checklist:
        await db.delete(checklist)

    await db.delete(db_recebimento)
    await commit_or_rollback(db)

    return db_recebimento


@router.post("/upload_foto")
async def upload_foto(
    item_recebimento_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
):
    """
    Faz o upload de uma foto para o item de recebimento.

    :param item_recebimento_id: ID do item de recebimento.
    :param file: Arquivo de foto a ser enviado.
    :param db: Sessão do banco de dados.
    :return: A foto salva no banco.
    """
    try:
        file_location = f"fotos/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        foto = FotoRecebimento(
            url_foto=file_location, item_recebimento_id=item_recebimento_id
        )
        db.add(foto)
        await db.commit()
        await db.refresh(foto)

        return foto
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar foto: {str(e)}")
