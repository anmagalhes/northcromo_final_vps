from flask import Blueprint, jsonify, request
from .funcionario import list_funcionarios, get_funcionario, create_funcionario, update_funcionario, delete_funcionario

funcionario_blueprint = Blueprint('funcionario', __name__)

# Rota para listar todos os funcionários
@funcionario_blueprint.route('/', methods=['GET'])
def get_all_funcionarios():
    funcionarios = list_funcionarios()
    return jsonify(funcionarios), 200

# Rota para pegar os detalhes de um funcionário específico
@funcionario_blueprint.route('/<int:funcionario_id>', methods=['GET'])
def get_funcionario_details(funcionario_id):
    funcionario = get_funcionario(funcionario_id)
    if funcionario:
        return jsonify(funcionario), 200
    return jsonify({"message": "Funcionário não encontrado!"}), 404

# Rota para criar um novo funcionário
@funcionario_blueprint.route('/', methods=['POST'])
def create_new_funcionario():
    data = request.get_json()
    funcionario = create_funcionario(data)
    return jsonify(funcionario), 201

# Rota para atualizar um funcionário
@funcionario_blueprint.route('/<int:funcionario_id>', methods=['PUT'])
def update_funcionario_details(funcionario_id):
    data = request.get_json()
    updated_funcionario = update_funcionario(funcionario_id, data)
    if updated_funcionario:
        return jsonify(updated_funcionario), 200
    return jsonify({"message": "Funcionário não encontrado!"}), 404

# Rota para deletar um funcionário
@funcionario_blueprint.route('/<int:funcionario_id>', methods=['DELETE'])
def delete_funcionario_by_id(funcionario_id):
    if delete_funcionario(funcionario_id):
        return jsonify({"message": "Funcionário excluído com sucesso!"}), 200
    return jsonify({"message": "Funcionário não encontrado!"}), 404
