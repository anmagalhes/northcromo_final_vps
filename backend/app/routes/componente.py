from flask import Blueprint, request, jsonify
from ..componente import componente_blueprint
from ..componente.componente import list_componentes, get_componente, create_componente, update_componente, delete_componente

# Rota para listar todos os componentes
@componente_blueprint.route('/', methods=['GET'])
def get_all_componentes():
    componentes = list_componentes()
    return jsonify(componentes), 200

# Rota para obter um componente específico
@componente_blueprint.route('/<int:id>', methods=['GET'])
def get_componente_details(id):
    componente = get_componente(id)
    if componente:
        return jsonify(componente), 200
    return jsonify({"message": "Componente não encontrado!"}), 404

# Rota para criar um novo componente
@componente_blueprint.route('/', methods=['POST'])
def create_new_componente():
    data = request.get_json()
    componente = create_componente(data)
    return jsonify(componente), 201

# Rota para atualizar um componente existente
@componente_blueprint.route('/<int:id>', methods=['PUT'])
def update_componente_details(id):
    data = request.get_json()
    updated_componente = update_componente(id, data)
    if updated_componente:
        return jsonify(updated_componente), 200
    return jsonify({"message": "Componente não encontrado!"}), 404

# Rota para deletar um componente
@componente_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_componente_by_id(id):
    if delete_componente(id):
        return jsonify({"message": "Componente excluído com sucesso!"}), 200
    return jsonify({"message": "Componente não encontrado!"}), 404
