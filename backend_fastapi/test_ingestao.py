import requests
import pytest
from datetime import datetime

# URL da sua API
BASE_URL = "http://127.0.0.1:8000/recebimentos/"

# Definir os dados de entrada para o teste
data = [
    {
        "id": 0,
        "tipo_ordem": "NAO",
        "numero_ordem": 0,
        "recebimento_ordem": "string",
        "queixa_cliente": "string",
        "data_prazo_desmont": "2025-01-09T20:15:19.446Z",  # Certifique-se que este é o formato esperado
        "referencia_produto": "string",
        "numero_nota_fiscal": "string",
        "sv_desmontagem_ordem": "NAO",
        "sv_montagem_teste_ordem": "NAO",
        "limpeza_quimica_ordem": "NAO",
        "laudo_tecnico_ordem": "NAO",
        "desmontagem_ordem": "NAO",
        "data_rec_ordem": "2025-01-09T20:15:19.446Z",
        "hora_inicial_ordem": "2025-01-09T20:15:19.446Z",
        "data_final_ordem": "2025-01-09T20:15:19.446Z",
        "hora_final_ordem": "2025-01-09T20:15:19.446Z",
        "img1_ordem": "string",
        "img2_ordem": "string",
        "img3_ordem": "string",
        "img4_ordem": "string",
        "created_at": "2025-01-09T20:15:19.446Z",
        "updated_at": "2025-01-09T20:15:19.446Z",
        "deleted_at": "2025-01-09T20:15:19.446Z",
        "usuario_id": 0,
        "cliente_id": 0,
        "status_ordem": "PENDENTE",
        "itens": [
            {
                "qtd_produto": 0,
                "preco_unitario": 0,
                "preco_total": 0,
                "referencia_produto": "string",
                "status_ordem": "PENDENTE",
                "produto_id": 0,
                "recebimento_id": 0,
                "funcionario_id": 0,
                "created_at": "2025-01-09T20:15:19.446Z",
                "updated_at": "2025-01-09T20:15:19.446Z",
                "fotos": [],
                "produto": {
                    "codigo": 0,
                    "nome_produto": "string",
                    "und_servicos": "string",
                    "usuario_id": 0,
                    "componente_id": 0,
                    "operacao_id": 0,
                    "grupo_produto_id": 0,
                    "posto_trabalho_id": 0,
                    "created_at": "2025-01-09T20:15:19.446Z",
                    "updated_at": "2025-01-09T20:15:19.446Z",
                    "deleted_at": "2025-01-09T20:15:19.446Z",
                },
                "funcionario": {"nome": "string", "cargo": "string"},
            }
        ],
    }
]


# Função de teste de ingestão
@pytest.mark.parametrize("data", data)
def test_ingestao_dados(data):
    # Token de autenticação (substitua pelo seu token)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzM5MDQyNjc1LCJpYXQiOjE3MzY0NTA2NzUsInN1YiI6IjEifQ.5QDmurN0c-AoqX3_xtLmEXCBIuTqn46JbK21FxfofeQ"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Enviar a requisição POST com os dados
    response = requests.post(BASE_URL, json=data, headers=headers)

    # Verificar o status da resposta
    assert response.status_code == 200, f"Erro ao salvar: {response.text}"

    # Opcional: Verificar se a resposta contém algum dado esperado
    assert "id" in response.json(), "ID não foi retornado"
    print("Dado inserido com sucesso!")
