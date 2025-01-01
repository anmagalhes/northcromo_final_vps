from fastapi import APIRouter, Depends, HTTPException, status
from models.artigo import ArtigoModel
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.desp import get_current_user, get_session
from app.schema.artigo__schema import ArtigoSchema

router = APIRouter(prefix="/artigo", tags=["artigo"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def teste_artigo(
    artigo: ArtigoSchema,
    usuario_logado: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    try:
        # Criação de um novo ArtigoModel
        novo_artigo: ArtigoModel = ArtigoModel(
            titulo=artigo.titulo, usuario_id=usuario_logado.id
        )

        # Adicionando o artigo ao banco de dados
        db.add(novo_artigo)
        await db.commit()  # Confirmação da transação

        # Recuperando o artigo recém-adicionado com base no ID
        await db.refresh(
            novo_artigo
        )  # Garantir que o artigo tenha os dados atualizados após o commit

        # Retornando o ArtigoSchema baseado no ArtigoModel
        return ArtigoSchema.from_orm(novo_artigo)

    except SQLAlchemyError as e:
        # Caso ocorra um erro no banco de dados, podemos retornar uma mensagem mais amigável
        await db.rollback()  # Rollback da transação em caso de erro
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar salvar o artigo no banco de dados. Por favor, tente novamente mais tarde.",
            headers={
                "X-Error": str(e)
            },  # Incluindo o erro real nos headers, se necessário
        )

    except Exception as e:
        # Capturando outros tipos de erro
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ocorreu um erro ao tentar criar o artigo: {str(e)}",
        )


@router.get("/", response_model=list[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    try:
        # Criando a consulta
        query = select(ArtigoModel)

        # Executando a consulta
        result = await db.execute(query)

        # Obtendo todos os artigos (usando scalars() para pegar os resultados)
        artigos = result.scalars().all()

        # Caso não tenha artigos, retornamos um erro 404
        if not artigos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum artigo encontrado.",
            )

        # Retornando os artigos encontrados
        return [ArtigoSchema.from_orm(artigo) for artigo in artigos]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao tentar recuperar os artigos: {str(e)}",
        )


"""
# Endpoint GET para listar os artigos de um usuário
@router.get('/', status_code=status.HTTP_200_OK, response_model=list[ArtigoSchema])
async def get_artigos(usuario_logado: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    try:
        # Consultando os artigos do usuário logado
        result = await db.execute(select(ArtigoModel).filter(ArtigoModel.usuario_id == usuario_logado.id))
        artigos = result.scalars().all()  # Retorna todos os artigos para o usuário logado
        
        # Verificando se há artigos
        if not artigos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum artigo encontrado para o usuário.",
            )
        
        # Retornando a lista de artigos como ArtigoSchema
        return [ArtigoSchema.from_orm(artigo) for artigo in artigos]
    
    except Exception as e:
        # Tratando erros não relacionados ao banco de dados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao tentar recuperar os artigos: {str(e)}",
        )

"""
