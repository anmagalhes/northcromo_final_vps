import pandas as pd
from io import BytesIO
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cliente import Cliente
from app.models.user import User
from core.desp import get_current_user, get_session
import re
from fastapi import Query
from sqlalchemy import select


router = APIRouter(prefix="/cliente/importar", tags=["importação de clientes"])

# Criando variáveis para dependências com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# Função para validar CPF/CNPJ (aqui simplificada, você pode usar uma biblioteca como 'validate_docbr' para validação completa)
def validar_documento(doc: str) -> bool:
    # Exemplo simples de validação de CPF
    return (
        re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", doc) is not None
        or re.match(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", doc) is not None
    )


# Função para validar telefone
def validar_telefone(telefone: str) -> bool:
    return re.match(r"^\(?\d{2}\)?\s?\d{4,5}-\d{4}$", telefone) is not None


@router.post("/", response_model=dict)
async def import_clientes(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    file: UploadFile = File(...),  # Arquivo enviado pelo usuário
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    try:
        # Lê o conteúdo do arquivo enviado
        contents = await file.read()

        if file.filename.endswith(".csv"):
            # Lê arquivo CSV
            df = pd.read_csv(BytesIO(contents))
        elif file.filename.endswith(".xlsx"):
            # Lê arquivo Excel
            df = pd.read_excel(BytesIO(contents))
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de arquivo inválido. Apenas CSV ou Excel são suportados.",
            )

        # Verifica se o arquivo contém as colunas necessárias
        required_columns = [
            "nome_cliente",
            "doc_cliente",
            "endereco_cliente",
            "num_cliente",
            "bairro_cliente",
            "cidade_cliente",
            "uf_cliente",
            "cep_cliente",
            "telefone_cliente",
        ]

        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A coluna '{col}' não foi encontrada no arquivo.",
                )

        # Verifica e formata os dados antes de inserir no banco
        for index, row in df.iterrows():
            nome_cliente = (
                row["nome_cliente"].strip()
                if isinstance(row["nome_cliente"], str)
                else None
            )
            doc_cliente = (
                row["doc_cliente"].strip()
                if isinstance(row["doc_cliente"], str)
                and validar_documento(row["doc_cliente"])
                else None
            )
            endereco_cliente = (
                row["endereco_cliente"].strip()
                if isinstance(row["endereco_cliente"], str)
                else None
            )
            num_cliente = str(
                row["num_cliente"]
            ).strip()  # Convertendo para string para garantir que o número seja tratado corretamente
            bairro_cliente = (
                row["bairro_cliente"].strip()
                if isinstance(row["bairro_cliente"], str)
                else None
            )
            cidade_cliente = (
                row["cidade_cliente"].strip()
                if isinstance(row["cidade_cliente"], str)
                else None
            )
            uf_cliente = (
                row["uf_cliente"].strip()
                if isinstance(row["uf_cliente"], str)
                else None
            )
            cep_cliente = (
                row["cep_cliente"].strip()
                if isinstance(row["cep_cliente"], str)
                else None
            )
            telefone_cliente = (
                row["telefone_cliente"].strip()
                if isinstance(row["telefone_cliente"], str)
                and validar_telefone(row["telefone_cliente"])
                else None
            )

            if not all(
                [
                    nome_cliente,
                    doc_cliente,
                    endereco_cliente,
                    num_cliente,
                    bairro_cliente,
                    cidade_cliente,
                    uf_cliente,
                    cep_cliente,
                    telefone_cliente,
                ]
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Dados inválidos no arquivo, verifique as colunas.",
                )

            db_cliente = Cliente(
                nome_cliente=nome_cliente,
                doc_cliente=doc_cliente,
                endereco_cliente=endereco_cliente,
                num_cliente=num_cliente,
                bairro_cliente=bairro_cliente,
                cidade_cliente=cidade_cliente,
                uf_cliente=uf_cliente,
                cep_cliente=cep_cliente,
                telefone_cliente=telefone_cliente,
                usuario_id=user.id,  # Associando o cliente ao usuário autenticado
            )
            db.add(db_cliente)

        # Commit para salvar no banco de dados
        await db.commit()
        return {"status": "Importação realizada com sucesso!"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar o arquivo: {str(e)}",
        )
