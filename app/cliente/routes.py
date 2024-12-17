from flask import jsonify, request
from . import cliente_blueprint
from .services import list_clientes, get_cliente, create_cliente, update_cliente, delete_cliente

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

# Rota para criar um novo cliente
@cliente_blueprint.route('/', methods=['POST'])
def create_new_cliente():
    data = request.get_json()  # Recebe os dados JSON enviados na requisição
    cliente = create_cliente(data)  # Cria um novo cliente
    return jsonify(cliente), 201

# Rota para atualizar um cliente
@cliente_blueprint.route('/<int:id>', methods=['PUT'])
def update_cliente_details(id):
    data = request.get_json()
    updated_cliente = update_cliente(id, data)
    if updated_cliente:
        return jsonify(updated_cliente), 200
    return jsonify({"message": "Cliente não encontrado!"}), 404

# Rota para deletar um cliente
@cliente_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_cliente_by_id(id):
    if delete_cliente(id):
        return jsonify({"message": "Cliente excluído com sucesso!"}), 200
    return jsonify({"message": "Cliente não encontrado!"}), 404
