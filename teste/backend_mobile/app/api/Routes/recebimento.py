from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import get_db
from app.api.models.recebimento import Recebimento
from app.Schema.recebimento_schema import LinksFotos, RecebimentoSchema
from typing import List

router = APIRouter()

@router.post("/salvarLinksFotos")
def salvar_links_fotos(link_data: LinksFotos, db: Session = Depends(get_db)):
    try:
        numero_ordem_int = int(link_data.numero_ordem)
    except ValueError:
        raise HTTPException(status_code=400, detail="Número da ordem deve ser um inteiro válido.")

    try:
        recebimento = db.query(Recebimento).filter(Recebimento.numero_ordem == numero_ordem_int).first()

        if not recebimento:
            # Cria um novo registro se não existir
            recebimento = Recebimento(
                numero_ordem=numero_ordem_int,
                img1_ordem=link_data.foto1,
                img2_ordem=link_data.foto2,
                img3_ordem=link_data.foto3,
                img4_ordem=link_data.foto4,
                cliente=link_data.cliente,
                quantidade=link_data.quantidade
            )
            db.add(recebimento)
        else:
            # Atualiza os campos se já existir
            recebimento.img1_ordem = link_data.foto1
            recebimento.img2_ordem = link_data.foto2
            recebimento.img3_ordem = link_data.foto3
            recebimento.img4_ordem = link_data.foto4
            recebimento.cliente = link_data.cliente
            recebimento.quantidade = link_data.quantidade

        db.commit()
        db.refresh(recebimento)

        return {"success": True, "message": "Dados processados com sucesso!", "data": recebimento}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")


@router.get("/verificarOrdem/{numero_ordem}")
def verificar_ordem(numero_ordem: int, db: Session = Depends(get_db)):
    try:
        recebimento = db.query(Recebimento).filter(Recebimento.numero_ordem == numero_ordem).first()

        if not recebimento:
            return {"exists": False, "message": f"Ordem {numero_ordem} não encontrada"}

        return {
            "exists": True,
            "data": {
                "numero_ordem": recebimento.numero_ordem,
                "cliente": getattr(recebimento, "cliente", None),  # protege caso cliente não exista
                "status": getattr(recebimento, "status", None),    # idem para status
            },
        }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")

@router.get("/listarLinksFotos", response_model=List[RecebimentoSchema])
def listar_links_fotos(db: Session = Depends(get_db)):
    try:
        dados = db.query(Recebimento).all()

        # Ajusta cada registro para garantir que quantidade seja int
        for item in dados:
            if not isinstance(item.quantidade, int):
                try:
                    item.quantidade = int(item.quantidade)
                except (ValueError, TypeError):
                    item.quantidade = 0  # Se não for possível converter, coloca 0

        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar os dados: {str(e)}")

