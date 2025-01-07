# app/controllers/checklist_controller.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.checklist_recebimento.checklist_recebimento import Checklist_Recebimento
from app.models.user import User
from app.schema.checklist_recebimento import (
    Checklist_RecebimentoPublic,
    Checklist_RecebimentoSchema,
    Checklist_RecebimentoList,
    Checklist_RecebimentoUpdate,
)
from core.desp import get_current_user, get_session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

router = APIRouter(prefix="/checklist", tags=["checklists"])

# Dependências para a sessão e usuário autenticado
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]

# CRIAR Checklist
@router.post("/", response_model=Checklist_RecebimentoPublic)
async def create_checklist(
    checklist: Checklist_RecebimentoSchema,  # Dados de entrada para criar o Checklist
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Criando um novo Checklist no banco de dados
    db_checklist = Checklist_Recebimento(
        nota_interna=checklist.nota_interna,
        referencia_produto=checklist.referencia_produto,
        status_tarefa=checklist.status_tarefa,
        observacao_checklist=checklist.observacao_checklist,
        hora_inicial_ordem=checklist.hora_inicial_ordem,
        datarec_ordem_servicos=checklist.datarec_ordem_servicos,
        usuario_id=user.id,  # Associando o Checklist ao usuário autenticado
        impresso=False,  # Inicialmente como não impresso
    )

    db.add(db_checklist)  # Adicionando o Checklist à sessão do banco
    await db.commit()  # Persistindo a transação
    await db.refresh(db_checklist)  # Atualizando o objeto com os dados persistidos (como o ID)

    return db_checklist  # Retornando o Checklist criado


# LISTAR Checklists
@router.get("/", response_model=Checklist_RecebimentoList)
async def list_checklists(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário atual autenticado
    offset: int = 0,  # Valor padrão para a paginação
    limit: int = 10,  # Valor padrão para a paginação
    status_tarefa: str | None = None,  # Filtro opcional pelo status da tarefa
    impresso: bool | None = None,  # Filtro opcional para verificar se foi impresso
):
    # Validação de valores de offset e limit
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

    # Criando a consulta para pegar todos os Checklists
    query = select(Checklist_Recebimento)

    # Filtro opcional pelo status da tarefa
    if status_tarefa:
        query = query.filter(Checklist_Recebimento.status_tarefa.ilike(f"%{status_tarefa}%"))

    # Filtro opcional pelo status de impressão
    if impresso is not None:
        query = query.filter(Checklist_Recebimento.impresso == impresso)

    # Paginação
    query = query.offset(offset).limit(limit)

    # Executando a consulta
    result = await db.execute(query)
    checklists = result.unique().scalars().all()

    if not checklists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum Checklist encontrado"
        )

    # Retorno dos resultados paginados
    return {"checklists": checklists, "offset": offset, "limit": limit}


# GERAR PDF DO CHECKLIST
@router.get("/{checklist_id}/gerar_pdf")
async def gerar_pdf_checklist(
    checklist_id: int,  # ID do Checklist para gerar o PDF
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o Checklist existe no banco de dados
    query = select(Checklist_Recebimento).where(Checklist_Recebimento.id == checklist_id)
    result = await db.execute(query)
    db_checklist = result.scalars().first()

    if not db_checklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist não encontrado.",
        )

    # Gerar PDF com os dados do Checklist
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Adicionando conteúdo no PDF (Exemplo simples)
    c.drawString(100, 750, f"Checklist ID: {db_checklist.id}")
    c.drawString(100, 730, f"Nota Interna: {db_checklist.nota_interna}")
    c.drawString(100, 710, f"Referência Produto: {db_checklist.referencia_produto}")
    c.drawString(100, 690, f"Status Tarefa: {db_checklist.status_tarefa}")
    c.drawString(100, 670, f"Observações: {db_checklist.observacao_checklist}")
    c.drawString(100, 650, f"Hora Inicial Ordem: {db_checklist.hora_inicial_ordem}")
    c.drawString(100, 630, f"Data Ordem Serviço: {db_checklist.datarec_ordem_servicos}")

    # Finalizando o PDF
    c.showPage()
    c.save()

    # Retornando o PDF gerado
    pdf_buffer.seek(0)
    return StreamingResponse(pdf_buffer, media_type="application/pdf")


# ALTERAR Checklist
@router.patch("/{checklist_id}", response_model=Checklist_RecebimentoPublic)
async def update_checklist(
    checklist_id: int,  # ID do Checklist a ser atualizado
    checklist: Checklist_RecebimentoSchema,  # Dados de entrada para atualizar o Checklist
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    checklist_update: Checklist_RecebimentoUpdate,
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verificando se o Checklist existe no banco de dados
    query = select(Checklist_Recebimento).where(Checklist_Recebimento.id == checklist_id)
    result = await db.execute(query)
    db_checklist = result.scalars().first()

    if not db_checklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist não encontrado.",
        )

    # Atualiza os campos com os dados enviados na requisição, se presentes
    update_data = checklist_update.dict(
        exclude_unset=True
    )  # Pega os dados que não são None
    for key, value in update_data.items():
        setattr(db_checklist, key, value)

    # Commit das mudanças no banco de dados
    await db.commit()

    # Refresca o objeto para garantir que ele tenha os dados mais recentes
    await db.refresh(db_checklist)

    # Retorna o Checklist atualizado
    return db_checklist


# DELETAR Checklist (opcional)
@router.delete("/{checklist_id}", response_model=Checklist_RecebimentoPublic)
async def delete_checklist(
    checklist_id: int,  # ID do Checklist a ser deletado
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    # Verifica se o Checklist existe no banco de dados
    query = select(Checklist_Recebimento).where(Checklist_Recebimento.id == checklist_id)
    result = await db.execute(query)
    db_checklist = result.scalars().first()

    if not db_checklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist não encontrado.",
        )

    # Deleta o Checklist do banco de dados
    await db.delete(db_checklist)
    await db.commit()

    return db_checklist  # Retorna o Checklist deletado
