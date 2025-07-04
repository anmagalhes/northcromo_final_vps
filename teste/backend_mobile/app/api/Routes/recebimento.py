from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import get_async_session
from app.api.models.recebimento import Recebimento
from app.Schema.recebimento_schema import LinksFotos, RecebimentoSchema
from typing import List
import re
from app.api.models.checklist_recebimento import ChecklistRecebimento
from app.api.models.notafiscal import NotaFiscal
from app.api.models.tarefa import Tarefa
from datetime import datetime

from app.api.models.enums import StatusTarefaEnum

router = APIRouter()

@router.post("/salvarLinksFotos")
async def salvar_links_fotos(link_data: LinksFotos, db: AsyncSession = Depends(get_async_session)):

    # Combinar data e hora em uma string
    data_hora_str = f"{link_data.dataRecebimento} {link_data.horaRecebimento}"

    # Converter para datetime (ajuste o formato conforme o padrão recebido)
    data_recebimento = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")

    # Validação do numero_ordem
    if not re.match(r'^\d+$', link_data.numero_ordem):
        raise HTTPException(status_code=400, detail="Número da ordem deve ser um inteiro válido.")

    numero_ordem_int = int(link_data.numero_ordem)

    # --- NOVO: trata nota fiscal ---
    nota_fiscal = None
    if link_data.nfRemessa:
        result_nf = await db.execute(
            select(NotaFiscal).filter(NotaFiscal.numero_nota_fiscal == link_data.nfRemessa)
        )
        nota_fiscal = result_nf.scalars().first()

        if not nota_fiscal:
            # Converte string "17/06/2025" para datetime.date
            data_emissao = datetime.strptime(link_data.dataRecebimento, "%d/%m/%Y").date()

            nota_fiscal = NotaFiscal(
            numero_nota_fiscal=link_data.nfRemessa,
                data_emissao=data_emissao

            )
            db.add(nota_fiscal)
            await db.flush()  # gera o ID para usar abaixo

    nota_fiscal_id = nota_fiscal.id if nota_fiscal else None
    # --- FIM do bloco nota fiscal --

    if numero_ordem_int == 0:
        # Se vier zero do front, cria direto um novo registro sem consultar o banco
        recebimento = Recebimento(
            numero_ordem=numero_ordem_int,
            img1_ordem=link_data.foto1,
            img2_ordem=link_data.foto2,
            img3_ordem=link_data.foto3,
            img4_ordem=link_data.foto4,
            cliente_id=link_data.cliente_id,
            quantidade=link_data.quantidade,
            tipo_ordem=link_data.tipoOrdem,
            os_formatado=link_data.os_formatado,
            queixa_cliente=link_data.queixa_cliente,
            nota_fiscal_id=nota_fiscal_id,
            data_recebimento=data_recebimento,
        )
        db.add(recebimento)
        await db.flush()

        checklist = ChecklistRecebimento(recebimento_id=recebimento.id)
        db.add(checklist)

    else:
        # Busca recebimento existente
        result = await db.execute(select(Recebimento).filter(Recebimento.numero_ordem == numero_ordem_int))
        recebimento = result.scalars().first()

        if not recebimento:
            recebimento = Recebimento(
                numero_ordem=numero_ordem_int,
                img1_ordem=link_data.foto1,
                img2_ordem=link_data.foto2,
                img3_ordem=link_data.foto3,
                img4_ordem=link_data.foto4,
                cliente_id=link_data.cliente_id,
                quantidade=link_data.quantidade,
                tipo_ordem=link_data.tipoOrdem,
                os_formatado=link_data.os_formatado,
                queixa_cliente=link_data.queixa_cliente,
                nota_fiscal_id=nota_fiscal_id,
                data_recebimento=data_recebimento,
            )
            db.add(recebimento)
            await db.flush()

            checklist = ChecklistRecebimento(recebimento_id=recebimento.id)
            db.add(checklist)

            #tarefa = ChecklistRecebimento(recebimento_id=recebimento.id)
            #db.add(tarefa)

        else:
            # Atualiza recebimento existente
            recebimento.img1_ordem = link_data.foto1
            recebimento.img2_ordem = link_data.foto2
            recebimento.img3_ordem = link_data.foto3
            recebimento.img4_ordem = link_data.foto4
            recebimento.cliente_id = link_data.cliente_id
            recebimento.quantidade = link_data.quantidade
            recebimento.tipo_ordem = link_data.tipoOrdem
            recebimento.os_formatado = link_data.os_formatado
            recebimento.queixa_cliente=link_data.queixa_cliente
            recebimento.nota_fiscal_id = nota_fiscal_id


    # Verifica checklist (se não existir, cria)
    result_checklist = await db.execute(select(ChecklistRecebimento).filter(ChecklistRecebimento.recebimento_id == recebimento.id))
    checklist = result_checklist.scalars().first()
    if not checklist:
        checklist = ChecklistRecebimento(recebimento_id=recebimento.id)
        db.add(checklist)
        await db.flush()

    # 🚨 Criação da nova tarefa vinculada ao recebimento
    result_tarefa = await db.execute(
        select(Tarefa).filter(Tarefa.recebimento_id == recebimento.id)
    )
    tarefa = result_tarefa.scalars().first()
    if not tarefa:
        tarefa = Tarefa(
            recebimento_id= recebimento.id,
            data_rec_ordem= recebimento.data_recebimento,
            qtde_servico=link_data.quantidade,
            id_servico=0,
            id_operacao=0,
            desc_servico_produto="Tarefa gerada automaticamente",
            status=StatusTarefaEnum.PENDENTE,
            referencia_produto=None,
            nota_interna=nota_fiscal_id,
            data_checklist_ordem=datetime.now(),
            checklistrecebimento_id=checklist.id,
        )
        db.add(tarefa)


    try:
        await db.commit()
        await db.refresh(recebimento)

        return {"success": True, "message": "Dados processados com sucesso!", "data": recebimento}

    except Exception as e:
        await db.rollback()
        import traceback
        print(traceback.format_exc())  # imprime a stack trace no console
        raise HTTPException(status_code=500, detail=f"Erro ao salvar os dados: {str(e)}")


@router.get("/verificarOrdem/{numero_ordem}")
async def verificar_ordem(numero_ordem: int, db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Recebimento).filter(Recebimento.numero_ordem == numero_ordem))
        recebimento = result.scalars().first()

        if not recebimento:
            return {"exists": False, "message": f"Ordem {numero_ordem} não encontrada"}

        return {
            "exists": True,
            "data": {
                "numero_ordem": recebimento.numero_ordem,
                "cliente": getattr(recebimento, "cliente", None),
                "status": getattr(recebimento, "status", None),
            },
        }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")


@router.get("/listarLinksFotos", response_model=List[RecebimentoSchema])
async def listar_links_fotos(db: AsyncSession = Depends(get_async_session)):
    try:
        result = await db.execute(select(Recebimento))
        dados = result.scalars().all()

        # Ajusta cada registro para garantir que quantidade seja int
        for item in dados:
            if not isinstance(item.quantidade, int):
                try:
                    item.quantidade = int(item.quantidade)
                except (ValueError, TypeError):
                    item.quantidade = 0  # fallback

        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar os dados: {str(e)}")
