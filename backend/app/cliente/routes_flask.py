# app/cliente/routes.py
from flask import jsonify, request
from ..main import db
from marshmallow import ValidationError
from . import cliente_blueprint
from .services import list_clientes, get_cliente, create_cliente, update_cliente, delete_cliente
from app.schemas.cliente import ClienteSchema

# Instância do schema teste
cliente_schema = ClienteSchema()  # Para operações com um único cliente
clientes_schema = ClienteSchema(many=True)  # Para listar múltiplos clientes

# Rota para listar todos os clientes
@cliente_blueprint.route('/', methods=['GET'])
def get_all_clientes():
    clientes = list_clientes()  # Chama a função que lista os clientes
    return jsonify(clientes), 200

# Rota para pegar detalhes de um cliente específico
@cliente_blueprint.route('/<int:id>', methods=['GET'])
def get_cliente_details(id):
    cliente = get_cliente(id)  # Chama a função que obtém os detalhes do cliente
    if cliente:
        return jsonify(cliente), 200
    return jsonify({"message": "Cliente não encontrado!"}), 404


@cliente_blueprint.route('/clientes', methods=['POST'])
def criar_cliente():
    try:
        # Recebe os dados JSON da requisição
        data = request.get_json()

        # Verifica se os dados foram recebidos corretamente
        if not data:
            return jsonify({"error": "Nenhum dado foi enviado."}), 400

        # Valida os dados usando o Marshmallow (usando load para validação e transformação)
        cliente_data = cliente_schema.load(data)  # Isso valida e retorna o objeto/dicionário carregado

        # Chama a função para criar o cliente, passando os dados validados
        cliente = create_cliente(cliente_data)

        # Se o retorno for um dicionário de erro (caso de falha)
        if isinstance(cliente, dict) and "error" in cliente:
            return jsonify(cliente), 400  # Aqui, o erro será retornado com status 400

        # Caso o cliente tenha sido criado com sucesso, retorna os dados do cliente com status 201
        return jsonify(cliente), 201

    except ValidationError as e:
        # Erro de validação do Marshmallow
        return jsonify({"error": "Dados inválidos", "details": e.messages}), 400

    except Exception as e:
        # Retorna erro genérico com a mensagem de exceção
        return jsonify({"error": f"Erro ao criar cliente: {str(e)}"}), 500

# Rota para atualizar um cliente
@cliente_blueprint.route('/<int:id>', methods=['PUT'])
def update_cliente_details(id):
    data = request.get_json()

    # Verifica se o cliente existe antes de tentar atualizar
    cliente = get_cliente(id)
    if not cliente:
        return jsonify({"message": "Cliente não encontrado!"}), 404

    # Valida os dados do cliente com o Marshmallow
    errors = cliente_schema.validate(data)
    if errors:
        return jsonify({"error": "Dados inválidos", "details": errors}), 400

    # Atualiza os dados do cliente
    updated_cliente = update_cliente(id, data)
    if updated_cliente:
        return jsonify(updated_cliente), 200
    return jsonify({"message": "Erro ao atualizar cliente"}), 500

# Rota para deletar um cliente
@cliente_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_cliente_by_id(id):
    if delete_cliente(id):
        return jsonify({"message": "Cliente excluído com sucesso!"}), 200
    return jsonify({"message": "Cliente não encontrado!"}), 404
