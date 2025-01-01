# app/controller/user.py
from typing import List

from core.desp import get_current_user, get_session
from core.security import gerar_hash_senha, verificar_senha
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.auth import autenticar, criar_token_acesso

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user_model import User
from app.schema.user import (
    UserPublicSchema,
    UserSchemaBase,
    UserSchemaCreate,
    UserSchemaUP,
)

router = APIRouter(prefix="/api/usuario", tags=["usuario"])


# GET LOGADO
@router.get("/logado", response_model=UserPublicSchema)
def get_logado(usuario_logado: User = Depends(get_current_user)):
    return usuario_logado


# POST /signup
@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=UserPublicSchema
)
async def post_usuario(
    usuario: UserSchemaCreate, db: AsyncSession = Depends(get_session)
):

    # Verifica se o username já existe
    stmt = select(User).filter(User.username == usuario.username)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Cria o novo usuário
    novo_usuario = User(
        username=usuario.username,
        email=usuario.email,
        password=gerar_hash_senha(usuario.password),  # Gera o hash da senha
        en_admin=usuario.en_admin,
    )

    # Adiciona o novo usuário ao banco de dados
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)  # Atualiza o objeto com os dados persistidos

    # Retorna o novo usuário (sem a senha, pois estamos usando UserSchemaBase)
    return novo_usuario


@router.get("/users", response_model=List[UserPublicSchema])
async def get_usuarios(
    limit: int = 10, skip: int = 0, db: AsyncSession = Depends(get_session)
):
    # Criando a consulta para garantir que os usuários sejam únicos (DISTINCT)
    stmt = select(User).distinct().offset(skip).limit(limit)
    result = await db.execute(stmt)
    users = result.scalars().all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )

    return users  # Retorna a lista de usuários com apenas username e email


@router.get("/users/{user_id}", response_model=UserPublicSchema)
async def get_usuario(user_id: int, db: AsyncSession = Depends(get_session)):
    # Consulta para buscar o usuário pelo ID
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()  # Retorna o primeiro usuário encontrado, ou None

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user  # Retorna o usuário com apenas os campos definidos em UserPublicSchema


# POST /login
@router.post("/login", response_model=UserPublicSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    # Autentica o usuário (verifica email e senha)
    usuario = await autenticar(form_data.username, form_data.password, db)

    # Se o usuário não for encontrado ou a senha estiver incorreta
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Dados de acesso incorretos.",  # Mensagem de erro personalizada
        )

    # Gera o token de acesso, passando o ID do usuário como 'sub'
    access_token = criar_token_acesso(
        sub=usuario.id
    )  # O 'sub' normalmente é o ID ou username do usuário

    # Retorna o token de acesso em formato JSON
    return JSONResponse(
        content={
            "access_token": access_token,  # O token gerado
            "token_type": "bearer",  # Tipo de token (bearer)
        },
        status_code=status.HTTP_200_OK,  # Código de resposta 200 OK
    )


@router.put("/update_user/{user_id}", response_model=UserPublicSchema)
async def update_usuario(
    user_id: int,
    usuario: UserSchemaUP,  # Usando o schema para dados de atualização
    db: AsyncSession = Depends(get_session),
):
    # Consulta para buscar o usuário pelo ID
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Atualizar apenas os campos que foram fornecidos no corpo da requisição
    if usuario.username:  # Atualizando o nome (username) se fornecido
        user.username = usuario.username

    if usuario.email:  # Atualizando o email se fornecido
        user.email = usuario.email

    if usuario.password:  # Atualizando a senha (com hash) se fornecido
        user.password = gerar_hash_senha(usuario.password)

    if usuario.eh_admin is not None:  # Atualizando o campo de admin, se fornecido
        user.eh_admin = usuario.eh_admin

    # Commit para salvar as alterações no banco de dados
    try:
        await db.commit()
        await db.refresh(user)  # Atualiza o objeto com os dados persistidos
    except Exception as e:
        await db.rollback()  # Reverte a transação em caso de erro
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the user",
        )

    # Retorna o usuário atualizado, sem a senha
    return user
