from flask import Blueprint, jsonify, request
from .services import list_grupo_produtos, get_grupo_produto, create_grupo_produto, update_grupo_produto, delete_grupo_produto

grupo_produto_blueprint = Blueprint('grupo_produto', __name__)

# Rota para listar todos os grupos de produtos
@grupo_produto_blueprint.route('/', methods=['GET'])
def get_all_grupo_produtos():
    grupo_produtos = list_grupo_produtos()  # Chama a função que lista os grupo_produtos
    return jsonify(grupo_produtos), 200

# Rota para pegar detalhes de um grupo de produto específico
@grupo_produto_blueprint.route('/<int:grupo_produto_id>', methods=['GET'])
def get_grupo_produto_details(grupo_produto_id):
    grupo_produto = get_grupo_produto(grupo_produto_id)  # Chama a função que obtém os detalhes do grupo_produto
    if grupo_produto:
        return jsonify(grupo_produto), 200
    return jsonify({"message": "Grupo de produto não encontrado!"}), 404

# Rota para criar um novo grupo de produto
@grupo_produto_blueprint.route('/', methods=['POST'])
def create_new_grupo_produto():
    data = request.get_json()  # Recebe os dados JSON enviados na requisição
    grupo_produto = create_grupo_produto(data)  # Cria um novo grupo_produto
    return jsonify(grupo_produto), 201

# Rota para atualizar um grupo de produto
@grupo_produto_blueprint.route('/<int:grupo_produto_id>', methods=['PUT'])
def update_grupo_produto_details(grupo_produto_id):
    data = request.get_json()
    updated_grupo_produto = update_grupo_produto(grupo_produto_id, data)
    if updated_grupo_produto:
        return jsonify(updated_grupo_produto), 200
    return jsonify({"message": "Grupo de produto não encontrado!"}), 404

# Rota para deletar um grupo de produto
@grupo_produto_blueprint.route('/<int:grupo_produto_id>', methods=['DELETE'])
def delete_grupo_produto_by_id(grupo_produto_id):
    if delete_grupo_produto(grupo_produto_id):
        return jsonify({"message": "Grupo de produto excluído com sucesso!"}), 200
    return jsonify({"message": "Grupo de produto não encontrado!"}), 404
