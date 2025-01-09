from typing import Annotated, List
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.recebimento import Recebimento, ItensRecebimento
from app.models.cliente import Cliente  # Modelo Cliente
from app.models.produto import Produto  # Modelo Produto
from app.models.user import User
from core.desp import get_current_user, get_session
import pandas as pd
from io import BytesIO
import re

router = APIRouter(prefix="/recebimentos/importar", tags=["Importação de Recebimentos"])

DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# Função para validar código (se necessário)
def validar_codigo(codigo: str) -> bool:
    return re.match(r"^\d+$", codigo) is not None


# Rota para download do modelo de importação
@router.get("/modelo", response_class=StreamingResponse)
async def download_modelo():
    model_data = {
        "tipo_ordem": ["OR001", "OR002", "OR003"],
        "numero_ordem": [123, 456, 789],
        "recebimento_ordem": ["01", "02", "03"],
        "data_rec_ordem": ["2023-01-01", "2023-02-01", "2023-03-01"],
        "cliente_nome": ["Cliente A", "Cliente B", "Cliente C"],  # Nome do cliente
        "cliente_email": [
            "clienteA@email.com",
            "clienteB@email.com",
            "clienteC@email.com",
        ],
        "cliente_endereco": ["Rua A", "Rua B", "Rua C"],
        "status_recebimento": [
            "Completo",
            "Pendente",
            "Em andamento",
        ],  # Status do recebimento
        "valor_total": [1000, 1500, 2000],  # Valor total do recebimento
        "itens": [
            [
                {
                    "produto_codigo": "P101",
                    "quantidade": 10,
                    "preco_unitario": 100,
                    "desconto": 0.1,
                }
            ],
            [
                {
                    "produto_codigo": "P102",
                    "quantidade": 15,
                    "preco_unitario": 150,
                    "desconto": 0.05,
                }
            ],
            [
                {
                    "produto_codigo": "P103",
                    "quantidade": 20,
                    "preco_unitario": 200,
                    "desconto": 0,
                }
            ],
        ],
    }

    df_model = pd.DataFrame(model_data)
    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_model.to_excel(writer, index=False, sheet_name="Modelo de Importação")

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=modelo_recebimentos.xlsx"
        },
    )


# Função para importar recebimentos a partir de um arquivo CSV ou Excel
@router.post("/", response_model=dict)
async def import_recebimentos(
    db: DbSession,
    user: Current_user,
    file: UploadFile = File(...),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    try:
        contents = await file.read()

        # Lê o arquivo dependendo da extensão (CSV ou Excel)
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(contents))
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de arquivo inválido. Apenas CSV ou Excel são suportados.",
            )

        # Normaliza as colunas para minúsculas
        df.columns = df.columns.str.lower()

        required_columns = [
            "tipo_ordem",
            "numero_ordem",
            "recebimento_ordem",
            "data_rec_ordem",
            "cliente_nome",  # Nome do cliente
            "cliente_email",
            "cliente_endereco",
            "status_recebimento",  # Status do recebimento
            "valor_total",  # Valor total
            "itens",
        ]

        # Verifica se o arquivo contém as colunas necessárias
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A coluna '{col}' não foi encontrada no arquivo.",
                )

        # Processa cada linha do arquivo
        for index, row in df.iterrows():
            tipo_ordem = row["tipo_ordem"].strip()
            numero_ordem = row["numero_ordem"]
            recebimento_ordem = row["recebimento_ordem"].strip()
            data_rec_ordem = row["data_rec_ordem"]
            cliente_nome = row["cliente_nome"]
            cliente_email = row["cliente_email"]
            cliente_endereco = row["cliente_endereco"]
            status_recebimento = row["status_recebimento"]
            valor_total = row["valor_total"]
            itens = row["itens"]

            # Busca o cliente pelo nome no banco de dados
            cliente = await db.execute(
                select(Cliente).where(Cliente.nome == cliente_nome)
            )
            cliente = cliente.scalars().first()

            if not cliente:
                # Se o cliente não existir, cria um novo cliente
                cliente = Cliente(
                    nome=cliente_nome, email=cliente_email, endereco=cliente_endereco
                )
                db.add(cliente)
                await db.commit()
                await db.refresh(
                    cliente
                )  # Para garantir que o ID do cliente foi gerado

            # Criação do recebimento
            db_recebimento = Recebimento(
                tipo_ordem=tipo_ordem,
                numero_ordem=numero_ordem,
                recebimento_ordem=recebimento_ordem,
                data_rec_ordem=data_rec_ordem,
                cliente_id=cliente.id,
                status_recebimento=status_recebimento,
                valor_total=valor_total,
            )
            db.add(db_recebimento)

            # Processamento dos itens do recebimento
            for item in itens:
                produto_codigo = item["produto_codigo"]
                quantidade = item["quantidade"]
                preco_unitario = item["preco_unitario"]
                desconto = item["desconto"]
                preco_total = quantidade * preco_unitario * (1 - desconto)

                # Busca o produto pelo código no banco de dados
                produto = await db.execute(
                    select(Produto).where(Produto.codigo == produto_codigo)
                )
                produto = produto.scalars().first()

                if not produto:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Produto com código '{produto_codigo}' não encontrado no banco de dados.",
                    )

                # Criação do item de recebimento
                db_item = ItensRecebimento(
                    produto_id=produto.id,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario,
                    preco_total=preco_total,
                    desconto=desconto,
                    recebimento_id=db_recebimento.id,
                )
                db.add(db_item)

        # Commit para salvar no banco de dados
        await db.commit()

        return {"status": "Importação de recebimentos realizada com sucesso!"}

    except Exception as e:
        # Log do erro no servidor
        print(f"Erro ao processar o arquivo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar o arquivo: {str(e)}",
        )
