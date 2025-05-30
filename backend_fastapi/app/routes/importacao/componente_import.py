# app/api/componente.py
from datetime import datetime
from io import BytesIO
import pandas as pd
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from psycopg2 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.componente import Componente
from app.models.grupo_produto import Grupo_Produto
from app.models.user import User

from core.desp import get_current_user, get_session
import re
from fastapi import Query
from sqlalchemy import select


router = APIRouter(prefix="/componente/importar", tags=["importação de componentes"])

# Criando variáveis para dependências com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# Função para validar o código do componente (pode ser adaptada)
def validar_codigo(codigo: str) -> bool:
    return re.match(r"^\d+$", codigo) is not None


# Função para validar o nome do componente
def validar_nome_componente(nome: str) -> bool:
    # Validando se o nome não está vazio e não é apenas espaços
    return bool(nome.strip())


# Função para validar o preço (simplificada)
def validar_preco(preco: float) -> bool:
    return preco >= 0


# Função para gerar o modelo de importação de componentes
@router.get("/modelo", response_class=StreamingResponse)
async def download_modelo():
    """
    Gera e retorna um arquivo Excel modelo contendo as colunas esperadas para
    a importação de componentes. O usuário pode baixar esse arquivo, preenchê-lo e enviá-lo
    para a importação de componentes.
    """
    # Exemplo de dados do modelo de importação, com colunas e exemplos de preenchimento
    model_data = {
        "nome_componente": [
            "Componente A",
            "Componente B",
            "Componente C",
        ],  # Exemplo de nome do componente
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
    worksheet.set_column("A:A", 30)  # Nome do Componente

    # Adicionando comentários explicativos em cada coluna
    worksheet.write_comment("A1", "Nome completo do componente (exemplo: Componente A)")

    output.seek(0)  # Necessário para retornar o arquivo gerado

    # Retornando o arquivo Excel como uma resposta de download
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=modelo_componentes.xlsx"},
    )


@router.post("/importar", response_model=dict)
async def import_funcionarios(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    file: UploadFile = File(...),  # Arquivo enviado pelo usuário
):
    """
    Importa funcionários a partir de um arquivo CSV ou Excel, validando os dados e associando
    a registros existentes no banco de dados, evitando a criação de duplicidade.
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    sucesso = []  # Lista para armazenar funcionários importados com sucesso
    falhas = []  # Lista para armazenar funcionários com falhas

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
        required_columns = ["nome", "cargo"]

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
                nome_funcionario = (
                    row["nome"].strip() if isinstance(row["nome"], str) else None
                )
                cargo_funcionario = (
                    row["cargo"].strip() if isinstance(row["cargo"], str) else None
                )

                # Valida os dados do funcionário
                if not nome_funcionario or not validar_nome(nome_funcionario):
                    falhas.append(
                        {
                            "linha": index + 1,
                            "motivo": f"Nome do funcionário inválido na linha {index + 1}.",
                        }
                    )
                    continue  # Continua para a próxima linha

                if not cargo_funcionario or not validar_cargo(cargo_funcionario):
                    falhas.append(
                        {
                            "linha": index + 1,
                            "motivo": f"Cargo inválido na linha {index + 1}.",
                        }
                    )
                    continue  # Continua para a próxima linha

                # Verifica se já existe um funcionário com o mesmo nome e cargo
                existing_funcionario = await db.execute(
                    select(Funcionario).filter(
                        Funcionario.nome == nome_funcionario,
                        Funcionario.cargo == cargo_funcionario,
                    )
                )
                if existing_funcionario.scalar() is not None:
                    falhas.append(
                        {
                            "linha": index + 1,
                            "motivo": f"Funcionário '{nome_funcionario}' já existe com o cargo '{cargo_funcionario}' na linha {index + 1}.",
                        }
                    )
                    continue  # Não cria duplicado, vai para a próxima linha

                # Criação do funcionário a ser inserido
                try:
                    db_funcionario = Funcionario(
                        nome=nome_funcionario,
                        cargo=cargo_funcionario,
                        usuario_id=user.id,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                    )
                    db.add(db_funcionario)
                    await db.flush()  # Empurra a transação para garantir visibilidade
                    sucesso.append(
                        {"linha": index + 1, "funcionario": nome_funcionario}
                    )
                except IntegrityError as e:
                    # Se ocorrer uma violação de chave única, será tratada aqui
                    falhas.append(
                        {
                            "linha": index + 1,
                            "motivo": f"Erro ao salvar o funcionário '{nome_funcionario}': {str(e)} na linha {index + 1}",
                        }
                    )

        # Commit de todos os funcionários ao banco de dados
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
