from typing import Annotated, List
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.recebimento import Recebimento
from app.models.itens_recebimento import ItensRecebimento
from app.models.user import User
from core.desp import get_current_user, get_session
from sqlalchemy.future import select
import pandas as pd
from io import BytesIO
import re

router = APIRouter(prefix="/recebimentos", tags=["Importação de Recebimentos"])

# Dependências para sessão de banco de dados e usuário autenticado
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# Função de validação para dados de recebimento (exemplo)
def validar_codigo(codigo: str) -> bool:
    return re.match(r"^\d+$", codigo) is not None


# Modelo de importação de recebimentos (como um arquivo Excel ou CSV)
@router.get("/modelo", response_class=StreamingResponse)
async def download_modelo():
    """
    Gera um arquivo Excel modelo para a importação de recebimentos.
    """
    model_data = {
        "tipo_ordem": ["OR001", "OR002", "OR003"],  # Exemplo de tipo de ordem
        "numero_ordem": [123, 456, 789],  # Exemplo de número de ordem
        "recebimento_ordem": ["01", "02", "03"],  # Exemplo de código de recebimento
        "data_rec_ordem": ["2023-01-01", "2023-02-01", "2023-03-01"],  # Exemplo de data
        "cliente_id": [1, 2, 3],  # Exemplo de ID de cliente
        "itens": [  # Exemplo de itens relacionados ao recebimento
            [{"produto_id": 101, "quantidade": 10, "preco_unitario": 100}],
            [{"produto_id": 102, "quantidade": 15, "preco_unitario": 150}],
            [{"produto_id": 103, "quantidade": 20, "preco_unitario": 200}],
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
        headers={"Content-Disposition": "attachment; filename=modelo_recebimentos.xlsx"},
    )


# Função para importar recebimentos a partir de arquivo CSV ou Excel
@router.post("/", response_model=dict)
async def import_recebimentos(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    file: UploadFile = File(...),  # Arquivo enviado pelo usuário
):
    """
    Importa recebimentos a partir de um arquivo CSV ou Excel.
    A função valida os dados, processa o arquivo e realiza a inserção no banco de dados.
    """
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

        # Normalizar as colunas para minúsculas
        df.columns = df.columns.str.lower()

        required_columns = [
            "tipo_ordem",
            "numero_ordem",
            "recebimento_ordem",
            "data_rec_ordem",
            "cliente_id",
            "itens"
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
            cliente_id = row["cliente_id"]
            itens = row["itens"]  # Assumindo que 'itens' seja uma lista de dicionários com detalhes dos itens

            # Valida os dados
            if not tipo_ordem or not numero_ordem or not recebimento_ordem or not data_rec_ordem:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Dados inválidos para o recebimento de número {numero_ordem}.",
                )

            # Criação do recebimento
            db_recebimento = Recebimento(
                tipo_ordem=tipo_ordem,
                numero_ordem=numero_ordem,
                recebimento_ordem=recebimento_ordem,
                data_rec_ordem=data_rec_ordem,
                cliente_id=cliente_id,
            )
            db.add(db_recebimento)

            # Processamento dos itens do recebimento
            for item in itens:
                produto_id = item["produto_id"]
                quantidade = item["quantidade"]
                preco_unitario = item["preco_unitario"]

                # Criação do item de recebimento
                db_item = ItensRecebimento(
                    produto_id=produto_id,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario,
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
