from typing import List
from fastapi import APIRouter, HTTPException
import pygsheets
from app.Schema.produto_tarefa import Produto_tarefaPublic, Produto_tarefaList
from pydantic import BaseModel

# Função que busca produtos do Google Sheets utilizando pygsheets
def get_produtos_from_sheets():
    # Autenticação com a Google Sheets API usando o Service Account
    gc = pygsheets.authorize(service_file='path_to_your_credentials.json')  # Substitua pelo caminho de suas credenciais

    # ID da planilha, extraído da URL que você forneceu
    sheet_id = '1ZcG0fYEEE80rTuEpM1dzP_bvI3CX1Jg2CfrhkWVzuJE'  # Substitua pelo ID real da sua planilha

    try:
        # Abra a planilha usando o ID
        sheet = gc.open_by_key(sheet_id).worksheet('Produto')  # 'Produto' é o nome da aba/worksheet
        rows = sheet.get_all_records()  # Obtém todos os registros (linhas) da planilha

        # Convertendo os dados para o formato que o modelo espera
        produtos = [
            {"codigo": str(row['Código']), "nome": row['Nome']}
            for row in rows
        ]

        return produtos

    except Exception as e:
        print(f"Erro ao acessar a planilha: {e}")
        raise HTTPException(status_code=500, detail="Erro ao acessar a planilha do Google Sheets")

# Criação do router para produtos
router = APIRouter(prefix="/produto", tags=["produtos"])

# Rota para listar todos os produtos
@router.get("/produtos", response_model=Produto_tarefaList)
async def get_produtos(offset: int = 0, limit: int = 10):
    produtos = get_produtos_from_sheets()

    # Paginação: aplica offset e limit
    produtos_paginados = produtos[offset: offset + limit]

    return Produto_tarefaList(
        produto_tarefas=[Produto_tarefaPublic(id=i + 1, name=p['nome']) for i, p in enumerate(produtos_paginados)],
        offset=offset,
        limit=limit
    )

# Rota para buscar um produto específico pelo código
@router.get("/produto/{codigo}", response_model=Produto_tarefaPublic)
async def get_produto(codigo: str):
    produtos = get_produtos_from_sheets()
    produto = next((p for p in produtos if p["codigo"] == codigo), None)

    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return Produto_tarefaPublic(id=1, name=produto['nome'])
