# app/services/foto_recebimento_service.py
from sqlalchemy.orm import Session
from app.models.recebimento.foto_recebimento import FotoRecebimento
from app.schemas.foto_recebimento import FotoRecebimentoCreate, FotoRecebimentoUpdate
from typing import List, Optional


def criar_foto_recebimento(
    db: Session, foto: FotoRecebimentoCreate, recebimento_id: int
) -> FotoRecebimento:
    db_foto = FotoRecebimento(
        id_ordem=foto.id_ordem, nome_foto=foto.nome_foto, recebimento_id=recebimento_id
    )
    db.add(db_foto)
    db.commit()
    db.refresh(db_foto)
    return db_foto


def listar_fotos_recebimento(db: Session, recebimento_id: int) -> List[FotoRecebimento]:
    return (
        db.query(FotoRecebimento)
        .filter(FotoRecebimento.recebimento_id == recebimento_id)
        .all()
    )


def atualizar_foto_recebimento(
    db: Session, foto_id: int, foto: FotoRecebimentoUpdate
) -> FotoRecebimento:
    db_foto = db.query(FotoRecebimento).filter(FotoRecebimento.id == foto_id).first()
    if db_foto:
        db_foto.id_ordem = foto.id_ordem
        db_foto.nome_foto = foto.nome_foto
        db.commit()
        db.refresh(db_foto)
    return db_foto


def deletar_foto_recebimento(db: Session, foto_id: int) -> Optional[FotoRecebimento]:
    db_foto = db.query(FotoRecebimento).filter(FotoRecebimento.id == foto_id).first()
    if db_foto:
        db.delete(db_foto)
        db.commit()
    return db_foto
