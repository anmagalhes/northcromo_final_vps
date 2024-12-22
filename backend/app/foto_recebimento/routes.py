from flask import jsonify, request
from . import foto_recebimento_blueprint
from .services import list_fotos, get_foto, create_foto, update_foto, delete_foto

# Rota para listar todas as fotos de recebimento
@foto_recebimento_blueprint.route('/', methods=['GET'])
def get_all_fotos():
    fotos = list_fotos()  # Chama a função que lista as fotos
    return jsonify(fotos), 200

# Rota para pegar detalhes de uma foto de recebimento específica
@foto_recebimento_blueprint.route('/<int:foto_id>', methods=['GET'])
def get_foto_details(foto_id):
    foto = get_foto(foto_id)  # Chama a função que obtém os detalhes da foto
    if foto:
        return jsonify(foto), 200
    return jsonify({"message": "Foto não encontrada!"}), 404

# Rota para criar uma nova foto de recebimento
@foto_recebimento_blueprint.route('/', methods=['POST'])
def create_new_foto():
    data = request.get_json()  # Recebe os dados JSON enviados na requisição
    foto = create_foto(data)  # Cria uma nova foto
    return jsonify(foto), 201

# Rota para atualizar uma foto de recebimento
@foto_recebimento_blueprint.route('/<int:foto_id>', methods=['PUT'])
def update_foto_details(foto_id):
    data = request.get_json()
    updated_foto = update_foto(foto_id, data)
    if updated_foto:
        return jsonify(updated_foto), 200
    return jsonify({"message": "Foto não encontrada!"}), 404

# Rota para deletar uma foto de recebimento
@foto_recebimento_blueprint.route('/<int:foto_id>', methods=['DELETE'])
def delete_foto_by_id(foto_id):
    if delete_foto(foto_id):
        return jsonify({"message": "Foto excluída com sucesso!"}), 200
    return jsonify({"message": "Foto não encontrada!"}), 404
