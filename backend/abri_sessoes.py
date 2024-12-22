from app import create_app, db  # Ou importe a função create_app e o db

def abrir_sessao():
    """Abrir a sessão do SQLAlchemy"""
    app = create_app()  # Cria a instância do app Flask
    with app.app_context():  # Garante que estamos no contexto da aplicação
        session = db.session  # Aqui você "abre" a sessão

        print("Sessão aberta com sucesso!")

# Chama a função para abrir a sessão
if __name__ == "__main__":
    abrir_sessao()  # Abre a sessão do SQLAlchemy
