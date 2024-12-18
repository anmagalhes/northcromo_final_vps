import logging
from app.models import User, db

# Configuração do logging
logging.basicConfig(level=logging.INFO)  # Para produção, use INFO ou WARNING

# Função para listar todos os usuários com paginação (melhoria de desempenho)
def list_users(page=1, per_page=10):
    try:
        users = User.query.paginate(page, per_page, False)  # Paginação para evitar carregamento de todos os usuários de uma vez
        return [user.to_dict() for user in users.items]  # Retorna os dados dos usuários paginados
    except Exception as e:
        logging.error(f"Erro ao listar os usuários: {e}")
        return []  # Retorna uma lista vazia em caso de erro

# Função para pegar detalhes de um usuário específico
def get_user(user_id):
    try:
        user = User.query.get(user_id)  # Busca o usuário pelo ID
        if user:
            return user.to_dict()  # Retorna os dados do usuário em formato de dicionário
        return None  # Retorna None se o usuário não for encontrado
    except Exception as e:
        logging.error(f"Erro ao obter o usuário com ID {user_id}: {e}")
        return None  # Retorna None se houver um erro inesperado

# Função para excluir um usuário
def delete_user(user_id):
    try:
        user = User.query.get(user_id)  # Busca o usuário pelo ID
        if user:
            db.session.delete(user)  # Deleta o usuário
            db.session.commit()  # Confirma a transação no banco
            logging.info(f"Usuário com ID {user_id} excluído com sucesso.")  # Log de sucesso
            return True  # Retorna True se o usuário foi excluído com sucesso
        logging.warning(f"Usuário com ID {user_id} não encontrado para exclusão.")  # Log de falha ao encontrar o usuário
        return False  # Retorna False se o usuário não for encontrado
    except Exception as e:
        db.session.rollback()  # Faz o rollback da transação em caso de erro
        logging.error(f"Erro ao excluir o usuário com ID {user_id}: {e}")  # Log do erro
        return False  # Retorna False caso ocorra um erro na exclusão
