from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.session import get_async_session
from app.api.models.recebimento import Recebimento

router = APIRouter()

@router.get("/ordemnova")
async def next_numero_ordem(db: AsyncSession = Depends(get_async_session)):
    try:
        # Executa a query async para pegar os numeros de ordem, ordenados
        result = await db.execute(select(Recebimento.numero_ordem).order_by(Recebimento.numero_ordem))
        numeros_ordem = result.scalars().all()

        # Encontre o próximo número disponível
        proximo_numero = 0  # Começa do zero

        for numero in numeros_ordem:
            if numero == proximo_numero:
                proximo_numero += 1
            else:
                break

        print(proximo_numero)

        return proximo_numero
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar o próximo número de ordem: {str(e)}")
