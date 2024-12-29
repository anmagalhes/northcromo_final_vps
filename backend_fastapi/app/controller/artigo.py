
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.desp import get_session, get_current_user
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from models.artigo import ArtigoModel
from models.user import User
from app.schema.artigo__schema import ArtigoSchema

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def teste_artigo(artigo: ArtigoSchema, usuario_logado: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    try:
        # Criação de um novo ArtigoModel
        novo_artigo: ArtigoModel = ArtigoModel(titulo=artigo.titulo, usuario_id=usuario_logado.id)

        # Adicionando o artigo ao banco de dados
        db.add(novo_artigo)
        await db.commit()  # Confirmação da transação

        # Recuperando o artigo recém-adicionado com base no ID
        await db.refresh(novo_artigo)  # Garantir que o artigo tenha os dados atualizados após o commit

        # Retornando o ArtigoSchema baseado no ArtigoModel
        return ArtigoSchema.from_orm(novo_artigo)
    
    except SQLAlchemyError as e:
        # Caso ocorra um erro no banco de dados, podemos retornar uma mensagem mais amigável
        await db.rollback()  # Rollback da transação em caso de erro
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar salvar o artigo no banco de dados. Por favor, tente novamente mais tarde.",
            headers={"X-Error": str(e)}  # Incluindo o erro real nos headers, se necessário
        )
    
    except Exception as e:
        # Capturando outros tipos de erro
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ocorreu um erro ao tentar criar o artigo: {str(e)}",
        )