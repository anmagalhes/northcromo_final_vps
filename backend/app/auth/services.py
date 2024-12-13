from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

# Função para criar usuário
def create_user(name, username, password):
    # Verificar se o usuário já existe
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return False

    # Criar o usuário
    new_user = User(name=name, username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return True

# Função para login (verificar senha)
def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return True
    return False
