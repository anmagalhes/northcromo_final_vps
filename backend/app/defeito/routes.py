from flask import jsonify, request
from app.models.defeito import Defeito
from app.schemas.defeito import DefeitoSchema
from . import defeito_blueprint
from .services import list_defeitos, get_defeito, create_defeito, update_defeito, delete_defeito


# Rota para listar todos os defeitos
@defeito_blueprint.route('/', methods=['GET'])
def get_all_defeitos():
    defeitos = list_defeitos()  # Chama a função que lista os defeitos
    return jsonify(defeitos), 200

# Rota para pegar detalhes de um defeito específico
@defeito_blueprint.route('/<int:defeito_id>', methods=['GET'])
def get_defeito_details(defeito_id):
    defeito = get_defeito(defeito_id)  # Chama a função que obtém os detalhes do defeito
    if defeito:
        return jsonify(defeito), 200
    return jsonify({"message": "Defeito não encontrado!"}), 404

# Rota para criar um defeito
@defeito_blueprint.route('/', methods=['POST'])
def create_new_defeito():
    data = request.get_json()  # Recebe os dados JSON enviados na requisição
    defeito = create_defeito(data)  # Cria um novo defeito
    return jsonify(defeito), 201

# Rota para atualizar um defeito
@defeito_blueprint.route('/<int:defeito_id>', methods=['PUT'])
def update_defeito_details(defeito_id):
    data = request.get_json()
    updated_defeito = update_defeito(defeito_id, data)
    if updated_defeito:
        return jsonify(updated_defeito), 200
    return jsonify({"message": "Defeito não encontrado!"}), 404

# Rota para deletar um defeito
@defeito_blueprint.route('/<int:defeito_id>', methods=['DELETE'])
def delete_defeito_by_id(defeito_id):
    if delete_defeito(defeito_id):
        return jsonify({"message": "Defeito excluído com sucesso!"}), 200
    return jsonify({"message": "Defeito não encontrado!"}), 404
