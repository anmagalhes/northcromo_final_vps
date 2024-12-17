from app.models import User, db

# Função para listar todos os usuários
def list_users():
    users = User.query.all()  # Pega todos os usuários
    return [user.to_dict() for user in users]  # Usa o método to_dict() de cada usuário

# Função para pegar detalhes de um usuário específico
def get_user(user_id):
    user = User.query.get(user_id)  # Busca o usuário pelo ID
    if user:
        return user.to_dict()  # Retorna os dados do usuário em formato de dicionário
    return None  # Retorna None se o usuário não for encontrado

# Função para excluir um usuário
def delete_user(user_id):
    user = User.query.get(user_id)  # Busca o usuário pelo ID
    if user:
        try:
            db.session.delete(user)  # Deleta o usuário
            db.session.commit()  # Confirma a transação no banco
            return True  # Retorna True se o usuário foi excluído com sucesso
        except Exception as e:
            db.session.rollback()  # Em caso de erro, faz o rollback da transação
            print(f"Erro ao excluir o usuário: {e}")
            return False  # Retorna False caso ocorra um erro
    return False  # Retorna False se o usuário não for encontrado