from app.main_validado import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Função para criar o usuário admin
def create_admin():
    # Inicializa o aplicativo Flask com o contexto adequado
    app = create_app()

    with app.app_context():  # Usa o contexto do aplicativo
        # Verifica se o usuário admin já existe
        admin_user = User.query.filter_by(username="admin").first()
        if not admin_user:
            # Cria o usuário admin
            admin_user = User(
                username="admin", 
                email="rhavitony@gmail.com", 
                name="Admin", 
                en_admin=True  # Configura o admin
            )
            admin_user.password = generate_password_hash("admin123")  # Criptografa a senha

            # Adiciona o usuário ao banco de dados
            db.session.add(admin_user)
            db.session.commit()
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe!")

# Chama a função para criar o usuário admin
if __name__ == '__main__':
    create_admin()
