from models import User, db

# Função para listar todos os usuários
def list_users():
    users = User.query.all()
    return [{"id": user.id, "name": user.name, "username": user.username} for user in users]

# Função para pegar detalhes de um usuário
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return {"id": user.id, "name": user.name, "username": user.username}
    return None

# Função para excluir um usuário
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
