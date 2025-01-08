# app/api/produto.py
from datetime import datetime
import pytz
from io import BytesIO
import pandas as pd
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.produto import Produto
from app.models.grupo_produto import Grupo_Produto
from app.models.componente import Componente
from app.models.operacao import Operacao
from app.models.postotrabalho import Postotrabalho
from app.models.user import User
from core.desp import get_current_user, get_session
import re

from fastapi import Query
from sqlalchemy.future import select 

router = APIRouter(prefix="/produto/importar", tags=["importação de produtos"])

# Criando variáveis para dependências com Annotated
DbSession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


# Função para validar o código de barras do produto (pode ser adaptada)
def validar_codigo(codigo: str) -> bool:
    return re.match(r"^\d+$", codigo) is not None


# Função para validar o preço (simplificada)
def validar_preco(preco: float) -> bool:
    return preco >= 0


# Função para gerar o modelo de importação de produtos
@router.get("/modelo", response_class=StreamingResponse)
async def download_modelo():
    """
    Gera e retorna um arquivo Excel modelo contendo as colunas esperadas para
    a importação de produtos. O usuário pode baixar esse arquivo, preenchê-lo e enviá-lo
    para a importação de produtos.

    **Resposta**
    - Retorna um arquivo Excel modelo para o usuário baixar.
    """
    # Exemplo de dados do modelo de importação, com colunas e exemplos de preenchimento
    model_data = {
        "codigo": ["12345", "12346", "12347"],  # Exemplo de código de produto
        "nome_produto": [
            "Produto A",
            "Produto B",
            "Produto C",
        ],  # Exemplo de nome de produto
        "und_servicos": ["un", "kg", "m2"],  # Exemplo de unidade de serviço
        "grupo_produto": [
            "Grupo 1",
            "Grupo 2",
            "Grupo 3",
        ],  # Exemplo de grupo de produto
        "componente": [
            "Componente 1",
            "Componente 2",
            "Componente 3",
        ],  # Exemplo de componente
        "operacao": ["Operação 1", "Operação 2", "Operação 3"],  # Exemplo de operação
        "posto_trabalho": [
            "Posto 1",
            "Posto 2",
            "Posto 3",
        ],  # Exemplo de posto de trabalho
        "descricao": [
            "Descrição Produto A",
            "Descrição Produto B",
            "Descrição Produto C",
        ],  # Descrição
        "preco_unitario": [10.5, 15.0, 7.25],  # Preço unitário
        "quantidade": [100, 200, 150],  # Quantidade disponível
        "categoria": [
            "Categoria A",
            "Categoria B",
            "Categoria C",
        ],  # Categoria do produto
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
    worksheet.set_column("A:A", 15)  # Código
    worksheet.set_column("B:B", 30)  # Nome do Produto
    worksheet.set_column("C:C", 15)  # Unidade
    worksheet.set_column("D:D", 20)  # Grupo Produto
    worksheet.set_column("E:E", 20)  # Componente
    worksheet.set_column("F:F", 20)  # Operação
    worksheet.set_column("G:G", 20)  # Posto de Trabalho
    worksheet.set_column("H:H", 40)  # Descrição
    worksheet.set_column("I:I", 10)  # Preço Unitário
    worksheet.set_column("J:J", 10)  # Quantidade
    worksheet.set_column("K:K", 20)  # Categoria

    # Adicionando comentários explicativos em cada coluna
    worksheet.write_comment("A1", "Código único do produto (exemplo: 12345)")
    worksheet.write_comment("B1", "Nome completo do produto (exemplo: Produto A)")
    worksheet.write_comment("C1", "Unidade de medida do produto (exemplo: un, kg, m2)")
    worksheet.write_comment(
        "D1", "Nome do grupo ao qual o produto pertence (exemplo: Grupo 1)"
    )
    worksheet.write_comment(
        "E1", "Nome do componente associado ao produto (exemplo: Componente 1)"
    )
    worksheet.write_comment(
        "F1", "Nome da operação de processamento do produto (exemplo: Operação 1)"
    )
    worksheet.write_comment(
        "G1", "Nome do posto de trabalho associado ao produto (exemplo: Posto 1)"
    )
    worksheet.write_comment(
        "H1", "Descrição detalhada do produto (exemplo: Descrição Produto A)"
    )
    worksheet.write_comment("I1", "Preço unitário do produto (exemplo: 10.5)")
    worksheet.write_comment(
        "J1", "Quantidade disponível para importação (exemplo: 100)"
    )
    worksheet.write_comment("K1", "Categoria do produto (exemplo: Categoria A)")

    output.seek(0)  # Necessário para retornar o arquivo gerado

    # Retornando o arquivo Excel como uma resposta de download
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=modelo_produtos.xlsx"},
    )


# Função para importação de produtos
@router.post("/", response_model=dict)
async def import_produtos(
    db: DbSession,  # Sessão do banco de dados
    user: Current_user,  # Usuário autenticado
    file: UploadFile = File(...),  # Arquivo enviado pelo usuário
):
    """
    Importa produtos a partir de um arquivo CSV ou Excel, validando os dados e associando
    a registros existentes no banco de dados.
    A função processa o arquivo, verifica a validade dos dados e realiza a inserção no banco
    de dados, associando cada produto a um grupo de produto, componente, operação e posto de trabalho.
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )

    try:
        contents = await file.read()

        # Lê arquivo dependendo da extensão (CSV ou Excel)
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
            "codigo", "nome_produto", "und_servicos", "grupo_produto", 
            "componente", "operacao", "posto_trabalho", "descricao", 
            "preco_unitario", "quantidade", "categoria"
        ]

        # Verifica se o arquivo contém as colunas necessárias
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A coluna '{col}' não foi encontrada no arquivo.",
                )

        # Carregar as entidades do banco (evitar múltiplas queries dentro do loop)
        grupo_produtos = {gp.name: gp for gp in await db.scalars(select(Grupo_Produto))}
        componentes = {comp.name: comp for comp in await db.scalars(select(Componente))}
        operacoes = {op.name: op for op in await db.scalars(select(Operacao))}
        postos_trabalho = {posto.name: posto for posto in await db.scalars(select(Postotrabalho))}

        # Processa cada linha do arquivo
        for index, row in df.iterrows():
            codigo = str(row["codigo"]).strip()
            nome_produto = row["nome_produto"].strip()
            und_servicos = row["und_servicos"].strip()
            grupo_produto_nome = row["grupo_produto"].strip()
            componente_nome = row["componente"].strip()
            operacao_nome = row["operacao"].strip()
            posto_trabalho_nome = row["posto_trabalho"].strip()
            descricao = row["descricao"].strip() if isinstance(row["descricao"], str) else None
            preco_unitario = row["preco_unitario"] if isinstance(row["preco_unitario"], (int, float)) else None
            quantidade = row["quantidade"] if isinstance(row["quantidade"], int) else None
            categoria = row["categoria"].strip()

            # Verifica se todas as informações necessárias estão presentes
            if not all([codigo, nome_produto, und_servicos, grupo_produto_nome, componente_nome, operacao_nome, posto_trabalho_nome]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Dados inválidos no arquivo para o produto {codigo}. Verifique as colunas.",
                )

            # Valida dados extras
            if not validar_preco(preco_unitario):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Preço inválido para o produto {codigo}.",
                )

            if not preco_unitario or not quantidade:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Preço ou quantidade ausentes para o produto {codigo}.",
                )

            # Busca as entidades relacionadas
            grupo_produto = grupo_produtos.get(grupo_produto_nome)
            componente = componentes.get(componente_nome)
            operacao = operacoes.get(operacao_nome)
            posto_trabalho = postos_trabalho.get(posto_trabalho_nome)

            # Valida se as entidades foram encontradas
            if not grupo_produto:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Grupo de produto '{grupo_produto_nome}' não encontrado.")
            if not componente:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Componente '{componente_name}' não encontrado.")
            if not operacao:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Operação '{operacao_nome}' não encontrada.")
            if not posto_trabalho:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Posto de trabalho '{posto_trabalho_nome}' não encontrado.")

            # Criação do produto a ser inserido
            db_produto = Produto(
                codigo=codigo,
                nome_produto=nome_produto,
                und_servicos=und_servicos,
                grupo_produto_id=grupo_produto.id,  # Associando o grupo_produto_id
                componente_id=componente.id,  # Associando o componente_id
                operacao_id=operacao.id,  # Associando o operacao_id
                posto_trabalho_id=posto_trabalho.id,  # Associando o posto_trabalho_id
                usuario_id=user.id,  # Associando o produto ao usuário autenticado
                descricao=descricao,
                preco_unitario=preco_unitario,
                quantidade=quantidade,
                categoria=categoria,
            )
            db.add(db_produto)

        # Commit para salvar no banco de dados
        await db.commit()

        return {"status": "Importação de produtos realizada com sucesso!"}

    except Exception as e:
        # Log do erro no servidor
        print(f"Erro ao processar o arquivo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar o arquivo: {str(e)}",
        )