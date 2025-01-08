# app/api/operacao.py
from datetime import datetime
from io import BytesIO
import pandas as pd
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from psycopg2 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.operacao import Operacao
from app.models.user import User
from core.desp import get_current_user, get_session
import re
from sqlalchemy import select


router = APIRouter(prefix="/operacao/importar", tags=["importação de operações"])

# Criando variáveis para dependências com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# Função para validar o nome da operação
def validar_nome_operacao(nome: str) -> bool:
    return bool(nome.strip())


# Função para validar o grupo da operação
def validar_grupo_operacao(grupo: str) -> bool:
    return bool(grupo.strip())


# Função para gerar o modelo de importação de operações
@router.get("/modelo", response_class=StreamingResponse)
async def download_modelo():
    """
    Gera e retorna um arquivo Excel modelo contendo as colunas esperadas para
    a importação de operações. O usuário pode baixar esse arquivo, preenchê-lo e enviá-lo
    para a importação de operações.
    """
    # Exemplo de dados do modelo de importação, com colunas e exemplos de preenchimento
    model_data = {
        "grupo_processo": [
            "Grupo A",
            "Grupo B",
            "Grupo C",
        ],  # Exemplo de grupo de processo
        "nome_processo": [
            "Operação A",
            "Operação B",
            "Operação C",
        ],  # Exemplo de nome de operação
    }

    # Convertendo o modelo para um DataFrame pandas
    df_model = pd.DataFrame(model_data)

    # Convertendo o DataFrame para um arquivo Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_model.to_excel(writer, index=False, sheet_name="Modelo de Importação")
    output.seek(0)  # Necessário para retornar o arquivo gerado

    # Acessando a aba da planilha
    worksheet = writer.sheets["Modelo de Importação"]

    # Ajustando a largura das colunas
    worksheet.set_column("A:A", 30)  # Grupo de Processo
    worksheet.set_column("B:B", 30)  # Nome do Processo

    # Adicionando comentários explicativos em cada coluna
    worksheet.write_comment("A1", "Grupo de processo (exemplo: Grupo A)")
    worksheet.write_comment("B1", "Nome da operação (exemplo: Operação A)")

    output.seek(0)  # Necessário para retornar o arquivo gerado

    # Retornando o arquivo Excel como uma resposta de download
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=modelo_operacoes.xlsx"},
    )


@router.post("/importar", response_model=dict)
async def import_operacoes(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    file: UploadFile = File(...),  # Arquivo enviado pelo usuário
):
    """
    Importa operações a partir de um arquivo CSV ou Excel, validando os dados e associando
    a registros existentes no banco de dados, evitando a criação de duplicidade.
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    sucesso = []  # Lista para armazenar operações importadas com sucesso
    falhas = []  # Lista para armazenar operações com falhas

    try:
        # Lê o conteúdo do arquivo enviado
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

        # Colunas necessárias para a validação
        required_columns = ["grupo_processo", "nome_processo"]

        # Verifica se o arquivo contém as colunas necessárias
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A coluna '{col}' não foi encontrada no arquivo.",
                )

        # Inicia a transação
        async with db.begin():  # Garante que as alterações sejam atômicas
            for index, row in df.iterrows():
                # Valida o nome da operação
                nome_processo = (
                    row["nome_processo"].strip()
                    if isinstance(row["nome_processo"], str)
                    else None
                )
                grupo_processo = (
                    row["grupo_processo"].strip()
                    if isinstance(row["grupo_processo"], str)
                    else None
                )

                # Verifica se todas as informações necessárias estão presentes
                if not nome_processo or not validar_nome_operacao(nome_processo):
                    falhas.append(
                        {
                            "linha": index + 1,
                            "motivo": f"Nome do processo inválido na linha {index + 1}.",
                        }
                    )
                    continue  # Continua para a próxima linha

                if not grupo_processo or not validar_grupo_operacao(grupo_processo):
                    falhas.append(
                        {
                            "linha": index + 1,
                            "motivo": f"Grupo de processo inválido na linha {index + 1}.",
                        }
                    )
                    continue  # Continua para a próxima linha

                # Verifica se já existe uma operação com o mesmo nome no banco de dados
                existing_operacao = await db.execute(
                    select(Operacao).filter(Operacao.name == nome_processo)
                )
                if existing_operacao.scalar() is not None:
                    falhas.append(
                        {
                            "linha": index + 1,
                            "motivo": f"Operação '{nome_processo}' já existe na linha {index + 1}.",
                        }
                    )
                    continue  # Não cria duplicado, vai para a próxima linha

                # Criação da operação a ser inserida
                try:
                    db_operacao = Operacao(
                        name=nome_processo,
                        grupo_operacao=grupo_processo,
                        usuario_id=user.id,
                        created_at=datetime.now(),  # Definindo a data e hora atual
                        updated_at=datetime.now(),  # Definindo a data e hora atual
                    )
                    db.add(db_operacao)
                    await db.flush()  # Empurra a transação para garantir visibilidade
                    sucesso.append({"linha": index + 1, "operacao": nome_processo})
                except IntegrityError as e:
                    # Se ocorrer uma violação de chave única, será tratada aqui
                    falhas.append(
                        {
                            "linha": index + 1,
                            "motivo": f"Erro ao salvar a operação '{nome_processo}': {str(e)} na linha {index + 1}",
                        }
                    )

        # Commit de todas as operações ao banco de dados
        if sucesso:
            await db.commit()

        # Se houver falhas, retorna os erros encontrados
        if falhas:
            return {
                "status": "Importação finalizada com erros",
                "sucesso": sucesso,
                "falhas": falhas,
            }

        # Caso contrário, retorno de sucesso total
        return {
            "status": "Importação finalizada com sucesso",
            "sucesso": sucesso,
            "falhas": [],
        }

    except Exception as e:
        # Tratamento de exceções genéricas
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar o arquivo: {str(e)}",
        )
