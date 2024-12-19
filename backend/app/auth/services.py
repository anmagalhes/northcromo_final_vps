# app/auth/services.py
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db  # Certifique-se de importar o modelo User

def create_user(username, email, password):
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def login_user(username, password):
    user = User.query.filter_by(username=username).first()  # Buscando o usuário
    if user and check_password_hash(user.password, password):  # Verifica a senha
        return user  # O login foi bem-sucedido, retorna o usuário
    return None  # Caso contrário, retorna None
