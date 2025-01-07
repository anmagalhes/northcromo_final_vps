# app/routes/recebimento.py
from typing import List
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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

router = APIRouter(prefix="/recebimentos", tags=["Recebimentos"])

# Criando uma variável para a dependência com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# Função para criar checklist e itens de recebimento
async def criar_checklist_e_itens(recebimento: Recebimento, db: AsyncSession):
    checklist = Checklist_Recebimento(
        recebimento_id=recebimento.id,
        datarec_ordem_servicos=recebimento.data_rec_ordem,
        hora_inicial_ordem=recebimento.hora_inicial_ordem,
        referencia_produto=recebimento.referencia_produto,
        nota_interna=f"Nota {recebimento.numero_nota_fiscal}",
        observacao_checklist="Observação inicial",
        status_tarefa="PENDENTE",
        data_checklist_ordem_servicos=recebimento.data_rec_ordem,
        cliente_id=recebimento.cliente_id,
        usuario_id=recebimento.usuario_id,
    )
    db.add(checklist)

    for item in recebimento.itens_recebimento:
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


# Rota para criar recebimento
# Rota para criar recebimento
@router.post("/", response_model=RecebimentoPublic)
async def create_recebimento(
    recebimento: RecebimentoSchema,  # Dados de entrada para criar o Recebimento
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    # Verifica se o usuário está autenticado
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Criar o recebimento
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

    db.add(db_recebimento)
    await db.commit()
    await db.refresh(db_recebimento)

    # Adicionar os itens de recebimento
    for item in recebimento.itens_recebimento:
        print(f"Item de recebimento: {item}")  # Depuração dos itens
        try:
            item_db = ItensRecebimento(
                qtd_produto=item.qtd_produto,
                preco_unitario=item.preco_unitario,
                preco_total=item.preco_total,
                referencia_produto=item.referencia_produto,
                status_ordem=item.status_ordem,
                produto_id=item.produto_id,
                recebimento_id=db_recebimento.id,
                funcionario_id=item.funcionario_id,
            )
            db.add(item_db)
        except Exception as e:
            print(f"Erro ao criar item de recebimento: {e}")
            raise HTTPException(
                status_code=500, detail="Erro ao criar item de recebimento."
            )

    await db.commit()

    # Criar checklist e itens associados
    await criar_checklist_e_itens(db_recebimento, db)

    return db_recebimento  # Retorna o recebimento criado


# Rota para listar recebimentos
@router.get("/", response_model=RecebimentoList)
async def list_recebimentos(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    cliente_id: int | None = None,  # Filtro opcional por cliente
    offset: int = 0,  # Valor padrão para a paginação
    limit: int = 10,  # Valor padrão para a paginação
):
    # Validação do offset e limit
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

    # Criando a consulta para pegar todos os Recebimentos
    query = select(Recebimento)

    # Filtros de busca
    if cliente_id:
        query = query.filter(Recebimento.cliente_id == cliente_id)

    # Paginação
    query = query.offset(offset).limit(limit)

    # Executando a consulta
    result = await db.execute(query)
    recebimentos = result.unique().scalars().all()

    if not recebimentos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum recebimento encontrado.",
        )

    # Retorno dos resultados paginados com o campo 'recebimentos'
    return {"recebimentos": recebimentos, "offset": offset, "limit": limit}


# Rota para atualizar recebimento
@router.patch("/{recebimento_id}", response_model=RecebimentoPublic)
async def update_recebimento(
    recebimento_id: int,
    recebimento: RecebimentoSchema,
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
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

    for key, value in recebimento.dict(exclude_unset=True).items():
        setattr(db_recebimento, key, value)

    await db.commit()
    await db.refresh(db_recebimento)

    return db_recebimento


# Criar itens para um recebimento específico
@router.post("/{recebimento_id}/itens", response_model=List[ItensRecebimentoSchema])
async def create_itens_recebimento(
    recebimento_id: int,  # ID do recebimento existente
    itens: List[ItensRecebimentoSchema],  # Lista de itens a serem adicionados
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o recebimento existe
    query = select(Recebimento).where(Recebimento.id == recebimento_id)
    result = await db.execute(query)
    db_recebimento = result.scalars().first()

    if not db_recebimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recebimento não encontrado."
        )

    # Criação dos itens de recebimento
    itens_db = []
    for item in itens:
        item_db = ItensRecebimento(
            qtd_produto=item.qtd_produto,
            preco_unitario=item.preco_unitario,
            preco_total=item.preco_total,
            referencia_produto=item.referencia_produto,
            status_ordem=item.status_ordem,
            produto_id=item.produto_id,
            recebimento_id=recebimento_id,  # Associar ao recebimento existente
            funcionario_id=item.funcionario_id,
        )
        itens_db.append(item_db)

    # Adicionando itens no banco de dados
    db.add_all(itens_db)
    await db.commit()

    # Retornando os itens criados
    return itens_db


# Rota para atualizar um item de recebimento
@router.patch(
    "/{recebimento_id}/itens/{item_id}", response_model=ItensRecebimentoSchema
)
async def update_item_recebimento(
    recebimento_id: int,  # ID do recebimento
    item_id: int,  # ID do item a ser atualizado
    item: ItensRecebimentoSchema,  # Dados de entrada para o item
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o recebimento existe
    query = select(Recebimento).where(Recebimento.id == recebimento_id)
    result = await db.execute(query)
    db_recebimento = result.scalars().first()

    if not db_recebimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recebimento não encontrado."
        )

    # Verifica se o item de recebimento existe
    query = select(ItensRecebimento).where(
        ItensRecebimento.id == item_id,
        ItensRecebimento.recebimento_id == recebimento_id,
    )
    result = await db.execute(query)
    db_item = result.scalars().first()

    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de recebimento não encontrado.",
        )

    # Atualiza o item com os novos dados
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    # Commit para salvar as alterações
    await db.commit()
    await db.refresh(db_item)

    return db_item


# Rota para deletar um item de recebimento
@router.delete(
    "/{recebimento_id}/itens/{item_id}", response_model=ItensRecebimentoSchema
)
async def delete_item_recebimento(
    recebimento_id: int,  # ID do recebimento
    item_id: int,  # ID do item a ser deletado
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o recebimento existe
    query = select(Recebimento).where(Recebimento.id == recebimento_id)
    result = await db.execute(query)
    db_recebimento = result.scalars().first()

    if not db_recebimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recebimento não encontrado."
        )

    # Verifica se o item de recebimento existe
    query = select(ItensRecebimento).where(
        ItensRecebimento.id == item_id,
        ItensRecebimento.recebimento_id == recebimento_id,
    )
    result = await db.execute(query)
    db_item = result.scalars().first()

    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de recebimento não encontrado.",
        )

    # Deleta o item de recebimento
    await db.delete(db_item)
    await db.commit()

    return db_item  # Retorna o item deletado


# Rota para deletar um recebimento
@router.delete("/{recebimento_id}", response_model=RecebimentoResponse)
async def delete_recebimento(
    recebimento_id: int,  # ID do recebimento a ser deletado
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o recebimento existe
    query = select(Recebimento).where(Recebimento.id == recebimento_id)
    result = await db.execute(query)
    db_recebimento = result.scalars().first()

    if not db_recebimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recebimento não encontrado."
        )

    # Deleta os itens de recebimento associados ao recebimento
    query_itens = select(ItensRecebimento).where(
        ItensRecebimento.recebimento_id == recebimento_id
    )
    result_itens = await db.execute(query_itens)
    itens = result_itens.scalars().all()

    for item in itens:
        await db.delete(item)

    # Deleta o checklist associado ao recebimento
    query_checklist = select(Checklist_Recebimento).where(
        Checklist_Recebimento.recebimento_id == recebimento_id
    )
    result_checklist = await db.execute(query_checklist)
    checklist = result_checklist.scalars().first()

    if checklist:
        await db.delete(checklist)

    # Deleta o recebimento
    await db.delete(db_recebimento)

    # Commit para salvar as exclusões no banco de dados
    await db.commit()

    return db_recebimento  # Retorna o recebimento deletado
