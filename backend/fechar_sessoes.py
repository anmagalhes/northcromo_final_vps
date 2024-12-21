from app import create_app, db  # Ou importe o db e a função de criar o app

def fechar_sessoes():
    """Fechar todas as sessões ativas do SQLAlchemy"""
    with app.app_context():  # Garante que estamos dentro do contexto da aplicação
        db.session.remove()  # Remove a sessão ativa
        print("Sessões fechadas com sucesso.")

# Chama a função para fechar as sessões
if __name__ == "__main__":
    app = create_app()  # Cria o app Flask
    fechar_sessoes()  # Fecha as sessões

