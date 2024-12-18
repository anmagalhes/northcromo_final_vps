# backend/app/user/routes.py

from flask import request, jsonify
from . import users_blueprint
from .services import list_users, get_user, delete_user

# Rota para listar todos os usuários
@users_blueprint.route('/', methods=['GET'])
def get_all_users():
    users = list_users()  # Chama a função que lista os usuários
    return jsonify(users), 200

# Rota para pegar detalhes de um usuário específico
@users_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    user = get_user(user_id)  # Chama a função que obtém os detalhes do usuário
    if user:
        return jsonify(user), 200
    return jsonify({"message": "Usuário não encontrado!"}), 404

# Rota para excluir um usuário
@users_blueprint.route('/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    if delete_user(user_id):  # Chama a função que exclui o usuário
        return jsonify({"message": "Usuário excluído com sucesso!"}), 200
    return jsonify({"message": "Usuário não encontrado!"}), 404
