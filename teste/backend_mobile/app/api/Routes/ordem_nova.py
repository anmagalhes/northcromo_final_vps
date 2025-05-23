from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import get_async_session
from app.api.models.recebimento import Recebimento
from app.Schema.recebimento_schema import LinksFotos, RecebimentoSchema
from typing import List

router = APIRouter()


@router.get("/ordemnova")
async def next_numero_ordem(db: Session = Depends(get_async_session)):
    try:
        # Obtenha todos os números de ordem existentes
        numeros_ordem = db.query(Recebimento.numero_ordem).order_by(Recebimento.numero_ordem).all()
        numeros_ordem = [num[0] for num in numeros_ordem]  # Extraia os números da lista de tuplas

        # Encontre o próximo número disponível
        proximo_numero = 1
        for numero in numeros_ordem:
            if numero == proximo_numero:
                proximo_numero += 1
            else:
                break

        return proximo_numero
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar o próximo número de ordem: {str(e)}")



